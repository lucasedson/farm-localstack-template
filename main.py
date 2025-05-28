import subprocess
import uuid
import json

id = lambda: str(uuid.uuid4())[:8]

aws = "awslocal"
def main():
    print(subprocess.check_output(f"{aws} --version", shell=True))


def EIPCreate():
    command = f"{aws} ec2 allocate-address --domain vpc --region us-east-1 --output json"
    eip = subprocess.check_output(command, shell=True)
    eip_json = json.loads(eip)
    return eip_json.get('AllocationId')

def make_east_1():    
    eip = EIPCreate()
    vpc_command = f"{aws} cloudformation deploy --region us-east-1 --template-file cloud-templates/vpc/vpc-template.yaml --stack-name vpc-stack-{id()} --parameter-overrides EIPAllocationId={eip}"
    subprocess.check_output(vpc_command, shell=True)

def run_cloudformation():
    make_east_1()

if __name__ == "__main__":
    main()
    run_cloudformation()
    # EIPCreate()
