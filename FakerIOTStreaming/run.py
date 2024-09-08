from faker_iot import FakerIot
import os
# Definir o caminho das credenciais do Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r""


run_faker = FakerIot(project_id="",
                     topic_id="",
                     time=4)

run_faker.start_streaming()
