import unittest

from server.service.file_formatter import convert_to_yaml, convert_to_dockerfile

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_to_yaml(self):
        sample_string = "```yaml\napiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: spring-boot-app\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: spring-boot-app\n  template:\n    metadata:\n      labels:\n        app: spring-boot-app\n    spec:\n      containers:\n      - name: spring-boot-app\n        image: your-docker-registry/spring-boot-app:latest\n        ports:\n        - containerPort: 8080\n        resources:\n          requests:\n            cpu: \"500m\"\n            memory: \"512Mi\"\n          limits:\n            cpu: \"1\"\n            memory: \"1Gi\"\n        env:\n        - name: SPRING_PROFILES_ACTIVE\n          value: \"prod\"\n        livenessProbe:\n          tcpSocket:\n            port: 8080\n          initialDelaySeconds: 15\n          periodSeconds: 20\n        readinessProbe:\n          tcpSocket:\n            port: 8080\n          initialDelaySeconds: 5\n          periodSeconds: 10\n```"

        # convert
        result_string = convert_to_yaml(sample_string)

        lines = result_string.split("\n")
        self.assertTrue(len(lines) > 5)
    
    def test_convert_to_dockerfile(self):
        sample_string = "```dockerfile\nFROM openjdk:24-ea-16-jdk-slim-bullseye\n\nWORKDIR /app\n\nCOPY pom.xml .\nRUN mvn dependency:go-offline\n\nCOPY src .\n\nRUN mvn package\n\nCMD [\"java\", \"-jar\", \"target/*.jar\"]\n```"

        #convert
        result_string = convert_to_dockerfile(sample_string)

        self.assertTrue("WORKDIR" in result_string)


if __name__ == '__main__':
    unittest.main()