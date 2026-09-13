"""Mechanical invocation adaptation of the preserved self-authored Python files.

Run only explicitly to regenerate fresh runtime sources in a new directory.
No mathematical function is called. Existing runtime files are never replaced.
The only AST changes are removal of the old argparse construction/dispatch and
replacement of the entry point by run(a) or run(args), supplied by the launcher.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def digest(b): return hashlib.sha256(b).hexdigest()
def dump(node): return ast.dump(node,include_attributes=False)
def parsing_assignment(node):
    return (isinstance(node,ast.Assign) and isinstance(node.value,ast.Call)
            and isinstance(node.value.func,ast.Attribute) and node.value.func.attr=='parse_args')
def adapt(text):
    tree=ast.parse(text); mains=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main']
    if len(mains)>1: raise ValueError('Ambiguous source entry point')
    body=mains[0].body if mains else tree.body
    indices=[i for i,n in enumerate(body) if parsing_assignment(n)]
    if not indices: return text,{'change':'none; import-safe mathematical module'}
    if len(indices)!=1: raise ValueError('Ambiguous argument parser binding')
    position=indices[0]; assignment=body[position]
    if len(assignment.targets)!=1 or not isinstance(assignment.targets[0],ast.Name): raise ValueError('Unexpected parser target')
    argument=assignment.targets[0].id
    retained=[n for n in body[position+1:] if not isinstance(n,(ast.FunctionDef,ast.Import,ast.ImportFrom))] if not mains else body[position+1:]
    prefix=[]
    for n in tree.body:
        if isinstance(n,(ast.Import,ast.ImportFrom)) or (isinstance(n,ast.FunctionDef) and n.name!='main') or isinstance(n,ast.ClassDef):
            prefix.append(copy.deepcopy(n))
        elif mains and not isinstance(n,(ast.If,ast.FunctionDef)):
            prefix.append(copy.deepcopy(n))
        elif not mains and isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):
            prefix.append(copy.deepcopy(n))
    function=ast.FunctionDef(name='run',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=argument)],kwonlyargs=[],kw_defaults=[],defaults=[]),
                             body=copy.deepcopy(retained),decorator_list=[])
    generated=ast.fix_missing_locations(ast.Module(body=[*prefix,function],type_ignores=[]))
    result=ast.unparse(generated)+'\n'
    reparsed=ast.parse(result); actual=next(n for n in reparsed.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    if [dump(n) for n in actual.body]!=[dump(n) for n in retained]: raise ValueError('Mathematical entry body changed')
    originals={n.name:dump(n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name!='main'}
    actual_helpers={n.name:dump(n) for n in reparsed.body if isinstance(n,ast.FunctionDef) and n.name!='run'}
    if originals!=actual_helpers: raise ValueError('A mathematical helper AST changed')
    return result,{'change':'Argument parsing removed; the unchanged entry body accepts one explicit namespace',
                   'argument':argument,'entry_body_ast_sha256':digest('\n'.join(map(dump,retained)).encode()),
                   'unchanged_helper_ast_sha256':{k:digest(v.encode()) for k,v in originals.items()}}

def main():
    target=HERE/'runtime'
    if target.exists(): raise ValueError('Runtime target must be fresh')
    source_map=json.loads((HERE/'SOURCE-MAP.json').read_text()); entries=[]
    for row in source_map['copies']:
        name=row['path'].removeprefix('originals/')
        if not name.endswith('.py') or name=='portable_run.py': continue
        p=HERE/row['path']; raw=p.read_bytes()
        if len(raw)!=row['bytes'] or digest(raw)!=row['sha256']: raise ValueError('Preserved source changed')
        text,change=adapt(raw.decode()); out=target/name; out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('x') as f:f.write(text)
        entries.append({'path':'runtime/'+name,'original':row['path'],'original_sha256':row['sha256'],
                        'bytes':out.stat().st_size,'sha256':digest(out.read_bytes()),**change})
    package=target/'slr_ehrhart/__init__.py'
    with package.open('x') as f:f.write('"""Clean portable namespace; the historical package initializer is not used."""\n')
    entries.append({'path':'runtime/slr_ehrhart/__init__.py','bytes':package.stat().st_size,'sha256':digest(package.read_bytes()),
                    'change':'New empty namespace; no historical package initializer copied or executed'})
    with (HERE/'RUNTIME-MAP.json').open('x') as f:json.dump({'schema':'portable-f025-runtime-v1','files':entries},f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps({'runtime_files':len(entries),'mathematical_functions_called':False}))

if __name__=='__main__':main()
