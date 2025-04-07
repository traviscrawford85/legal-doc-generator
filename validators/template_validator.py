# validators/template_validator.py

from jinja2 import Environment, meta

def get_template_variables(template_str: str) -> set:
    """
    Parses a Jinja template string and returns a set of all undeclared variables.
    """
    env = Environment()
    parsed_content = env.parse(template_str)
    return meta.find_undeclared_variables(parsed_content)

def _get_value_from_context(context: dict, variable: str) -> bool:
    """
    Traverse the context dict using a dotted variable name.
    Returns True if the variable exists, else False.
    """
    keys = variable.split(".")
    current = context
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    return True

def validate_template_against_context(template_str: str, context: dict) -> list:
    """
    Validates that all variables in the Jinja template exist in the context.
    
    Parameters:
        template_str: The Jinja template content as a string.
        context: The matter context as a dict.
    
    Returns:
        A list of missing variables (dotted paths) that are referenced in the template.
    """
    missing_vars = []
    variables = get_template_variables(template_str)
    for var in variables:
        if not _get_value_from_context(context, var):
            missing_vars.append(var)
    return missing_vars
