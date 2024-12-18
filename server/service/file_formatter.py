import yaml

def convert_to_yaml(yaml_string) -> str:
    # scrub the string
    # yaml_string = yaml_string.strip().replace("```yaml","").replace("```","") 
    yaml_string = yaml_string.strip().replace("```yaml","```") # remove the ```yaml part
    yaml_string = yaml_string.strip().split("```")[1] #return the code after the backtick block   
    # convert to yaml object
    yaml_data = yaml.safe_load(yaml_string)
    # send back as a 'clean' string
    clean_yaml_string = yaml.dump(yaml_data,default_flow_style=False)
    # return
    return clean_yaml_string

def convert_to_dockerfile(dockerfile_string) -> str:
    if "`" in dockerfile_string:
        # dockerfile_string = dockerfile_string.strip().replace("```dockerfile","").replace("```","")
        dockerfile_string = dockerfile_string.strip().split("```")[1] #return the code after the backtick block
        # split into lines
        lines = dockerfile_string.strip().split('\\n')
        # build
        dockerfile_content = '\n'.join(lines)
        # scrub
        dockerfile_content = dockerfile_content.strip()
        # return
        return dockerfile_content
    else:
        #return the string as is
        return dockerfile_string.strip()
    
