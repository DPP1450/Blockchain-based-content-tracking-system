from web3 import Web3
import json
import pathlib
import IPFS_API
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
assert web3.isConnected()

with open ("contract/abi.json") as f:
    contract_abi = f.read()
with open("config.json") as f:
    config = json.load(f)

contract_address = config["contract_address"]
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

private_key = "0x22aabb811efca4e6f4748bd18a46b502fa85549df9fa07da649c0a148d7d5530"
account = web3.eth.account.from_key(private_key)
web3.eth.default_account = account.address

def update_tx_params():
    global nonce
    global tx_params
    nonce = web3.eth.getTransactionCount(account.address)
    tx_params = {
        'nonce': nonce,
        'gasPrice': web3.eth.gas_price,
        'gas': 5000000, 
    }

def exp():
    print ("請輸入正確的選項\n")
    
def signUp():
    _name = input("enter user name or enter exit to cancel\n")
    if _name == "exit":
        return 
    update_tx_params()
    sign_up_tx = contract.functions.sign_up(_name).buildTransaction(tx_params)
    signed_tx = web3.eth.account.sign_transaction(sign_up_tx, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print ("tx_receipt : %s" % tx_receipt)
    except Exception as e:
        print (str(e).split("\'")[3])

def newProject():
    _name = input("enter project name or enter exit to cancel\n")
    if _name == "exit":
        return 
    update_tx_params()
    new_project_tx = contract.functions.new_project(_name).buildTransaction(tx_params)
    signed_tx = web3.eth.account.sign_transaction(new_project_tx, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print (str(e).split("\'")[3])

def listProject():
    print ("\n")
    projects = contract.functions.get_all_projects_name().call()
    for idx,p in enumerate(projects):
        print("%d. %s" % (idx+1,p))
    print ("\n")

def newCommit():
    listProject()
    projectidx = int(input("please select project or enter -1 to cancel\n"))
    if projectidx == -1:
        return 
    projects = contract.functions.get_all_projects_name().call()
    if (len(projects) < projectidx):
        print ("Index out of bound")
        return 
    log = input("please enter log or enter exit to cancel\n")
    if log == exit:
        return
    file_name = input("please enter filename or enter exit to cancel\n")
    if file_name == exit:
        return
    if not pathlib.Path(file_name).is_file():
        print ("file not found\n")
    cid = IPFS_API.Publish(file_name)
    print ("file upload to IPFS")
    print("cid : %s" % cid)  
    update_tx_params()
    new_commit_tx = contract.functions.new_commit(projectidx-1,cid,log).buildTransaction(tx_params)
    signed_tx = web3.eth.account.sign_transaction(new_commit_tx, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print (str(e).split("\'")[3])
    
def listCommit():
    projectidx = int(input("please select project\n"))
    projects = contract.functions.get_all_projects_name().call()
    if (len(projects) < projectidx):
        print ("Index out of bound")
        return 
    commits = contract.functions.get_all_commit_logs(projectidx-1).call()
    for idx,p in enumerate(commits):
        cid = contract.functions.get_ipfs_hash(projectidx-1 ,idx).call()
        print("%d. %s , cid : %s" % (idx+1,p,cid))
    print ("\n")

def addComment():

    commits = contract.functions.get_all_commit_ipfs().call()
    if len(commits) == 0:
        print ("no commit")
        return 
    for idx,p in enumerate(commits):
        print("%d. %s" % (idx+1,p))
    print ("\n")
    commitidx = int(input("please select commit or enter -1 to cancel\n"))
    if commitidx == -1:
        return 
    if (len(commits) < commitidx):
        print ("Index out of bound")
        return 

    commentMessage = input("please enter comment message or enter exit to cancel\n")
    if commentMessage == exit:
        return
    update_tx_params()
    new_comment_tx = contract.functions.new_comment(commitidx-1,commentMessage).buildTransaction(tx_params)
    signed_tx = web3.eth.account.sign_transaction(new_comment_tx, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    except Exception as e:
        print (str(e).split("\'")[3])

def listComment():
    listProject()
    projectidx = int(input("please select project or enter -1 to cancel\n"))
    if projectidx == -1:
        return 
    projects = contract.functions.get_all_projects_name().call()
    if (len(projects) < projectidx):
        print ("Index out of bound")
        return 

    commits = contract.functions.get_all_commit_logs(projectidx-1).call()
    if len(commits) == 0:
        print ("no commit")
        return 
    for idx,p in enumerate(commits):
        cid = contract.functions.get_ipfs_hash(projectidx-1 ,idx).call()
        print("%d. %s , cid : %s" % (idx+1,p,cid))
    print ("\n")
    commitidx = int(input("please select commit or enter -1 to cancel\n"))
    if commitidx == -1:
        return 
    if (len(commits) < commitidx):
        print ("Index out of bound")
        return 
    comments = contract.functions.get_comments(projectidx-1,commitidx-1).call()
    for idx,c in enumerate(comments):
        print("%d. %s "% (idx+1,c))
    print ("\n")
    

menu = "1. sign up\n2. new project\n3. list projects\n\
4. new commit\n5. list commit\n6. add comment\n7. list comment\n"
func = [exp, signUp, newProject, listProject,newCommit,listCommit,addComment,listComment]
while (1):
    i = int(input(menu))
    if (i < 0 or i >= len(func)):
        exp()
    else:
        func[i]()
