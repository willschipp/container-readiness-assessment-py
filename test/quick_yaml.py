import yaml

test_string = "```yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n name: spring-boot-app\n labels:\n app: spring-boot-app\nspec:\n replicas: 3 # Adjust the number of replicas as needed\n selector:\n matchLabels:\n app: spring-boot-app\n template:\n metadata:\n labels:\n app: spring-boot-app\n spec:\n containers:\n - name: spring-boot-app\n image: <YOUR_DOCKER_REGISTRY>/spring-boot-app:latest # REPLACE with your docker image\n ports:\n - containerPort: 8080 # Adjust if your application uses a different port\n livenessProbe:\n httpGet:\n path: /actuator/health # Assumes Spring Boot Actuator is included. Adjust path if needed.\n port: 8080\n initialDelaySeconds: 10\n periodSeconds: 5\n readinessProbe:\n httpGet:\n path: /actuator/health # Assumes Spring Boot Actuator is included. Adjust path if needed.\n port: 8080\n initialDelaySeconds: 10\n periodSeconds: 5\n resources:\n requests:\n cpu: 100m\n memory: 256Mi\n limits:\n cpu: 500m\n memory: 512Mi # Adjust resource limits based on your application's needs\n\n```\n\n**Before applying this:**\n\n1. **REPLACE `<YOUR_DOCKER_REGISTRY>/spring-boot-app:latest`:** This placeholder needs your actual Docker registry (e.g., `docker.io/yourusername/spring-boot-app:latest` or a private registry URL) and the correctly tagged Docker image. You'll need to build and push a Docker image of your Spring Boot application. A simple Dockerfile might look like this:\n\n```"

if "```yaml" in test_string:
    test_string = test_string.strip().replace("```yaml","```")

yaml_string = test_string.strip().split("```")[1] #return the code after the backtick block   

print(yaml_string)
# convert to yaml object
yaml_data = yaml.safe_load(yaml_string)
# send back as a 'clean' string
clean_yaml_string = yaml.dump(yaml_data,default_flow_style=False)

print(clean_yaml_string)