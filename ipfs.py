import IPFS_API
cid = IPFS_API.Publish('./test.txt')
print(cid)
print(IPFS_API.CatFile(cid).decode('UTF-8', 'ignore'))
