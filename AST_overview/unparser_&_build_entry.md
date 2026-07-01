  ''' _build_entry is a helper function. Its single job is to take one AST node (a function or a class from a Python file) and turn it into a neat dictionary that the rest of the tool can work with.
. The ast module gives you raw Python objects — _build_entry repacks them into a simple dictionary. Every function and class in the codebase will end up as one of these dictionaries.'''

def _build_entry(
    node: ast.FunctionDef | ast.ClassDef,  #function or class
    raw_source: str,  #entire file is just a big string , ast.get_source_segment needs raw text to extract code of this function or class 
    file_path: Path, 
    kind: str,        #doesnt itself figure out if its function or class , the caller tells it
) -> dict[str, Any]:
    
    doc = ast.get_docstring(node) or "" 
    
    lines = raw_source.splitlines(keepends=True) #spilt lines takes the entire text of source and breaks into lines , /n at the end 
    if source_code is None:
        source_code = ast.unparse(node)   #fallback
    
    return {
        "file_path": str(file_path.resolve()),
        "name": node.name,
        "kind": kind,
        "docstring": doc,
        "source": source_code,
        "line": node.lineno,
    }
    #return bundles everything together ....file_path_resolve will give absolute path


    #ast.unparse() converts ast node back into string of python
    # i think ast.get_source_segment ususally works but returns none in a few edge cases
    # in that case ast.unparse is a fallback , it recreates python code from the ast itself 
    # so youd never end up with none source. 
    # 
    # but the tradeoff is that unparse doesnt preserve origiinal formatting 
    # , comments or whitespace.
