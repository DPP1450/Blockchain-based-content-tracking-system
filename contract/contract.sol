// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.0 <0.9.0;

struct comment {
    string from;
    string comment;
}

contract commit {
    string ipfsHash;
    string log;
    uint time;
    comment[] public comments;

    constructor() {
        time = block.timestamp;
    }

    function add_comment(string memory from,string memory _comment) public {
        comment memory newComment = comment(from, _comment);
        comments.push(newComment);
    }

    function set_ipfs_hash(string memory _ipfsHash) public {
        ipfsHash = _ipfsHash;
    }

    function set_log(string memory _log) public {
        log = _log;
    }

    function get_ipfs_hash() public view returns (string memory) {
        return ipfsHash;
    }

    function get_log() public view returns (string memory) {
        return log;
    }

    function get_comments() public view returns (comment[] memory) {
        return comments;
    }
}

contract project {
    address owner;
    string projectName;
    commit[] commits;

    constructor(string memory _projectName, address _owner) {
        owner = _owner;
        projectName = _projectName;
    }

    function new_commit(string memory _ipfsHash, string memory _log) public {
        commit c = new commit();
        c.set_ipfs_hash(_ipfsHash);
        c.set_log(_log);
        commits.push(c);
    }

    function get_name() public view returns (string memory) {
        return projectName;
    }

    function get_all_commit_logs() public view returns(string[] memory){
        string[] memory logs = new string[](commits.length);
        for (uint i = 0 ; i < commits.length ; i++){
            logs[i] = commits[i].get_log();
        }
        return logs;
    }

    function get_commit(uint idx) public view returns(commit){
        if (idx + 1 > commits.length){
            revert("out of bound");
        }
        return commits[idx];
    }
}

contract user {
    string name;
    address addr;
    project[] projects;

    constructor(string memory _name, address _addr) {
        name = _name;
        addr = _addr;
    }

    function new_project(string memory _name) public {
        project p = new project(_name, addr);
        projects.push(p);
    }

    function get_name() public view returns (string memory) {
        return name;
    }

    function get_owner() public view returns (address) {
        return addr;
    }

    function get_all_projects_name() public view returns(string[] memory){
        string[] memory names = new string[](projects.length);
        for (uint i = 0 ; i < projects.length ; i++){
            names[i] = projects[i].get_name();
        }
        return names;
    }

    function get_project(uint idx) public view returns(project){
        if (idx + 1 > projects.length){
            revert("out of bound");
        }
        return projects[idx];
    }

}

contract controller {
    mapping(address => user) users;
    user[] userArray;

    modifier only_user {
        bool f = true;
        for (uint i = 0 ; i < userArray.length ; i++){
            if(userArray[i].get_owner() == msg.sender){
                f = false; 
            }  
        }
        if (f){
            revert("Please sign up");
        }
        _;
    }

    function sign_up(string memory _name) public {
        for (uint i = 0 ; i < userArray.length ; i++){
            require(userArray[i].get_owner() != msg.sender ,"You have already registered");
        }
        user u = new user(_name, msg.sender);
        users[msg.sender] = u;
        userArray.push(u);
    }

    function get_users() public view returns(string[] memory){
        string[] memory name = new string[](userArray.length);
        for (uint i = 0 ; i < userArray.length ; i++){
            name[i] = (userArray[i].get_name());
        }
        return name;
    }

    function new_project(string memory _name) public only_user{
        user u = users[msg.sender];
        u.new_project(_name);
    }

    function get_all_projects_name() public only_user view returns(string[] memory){
        user u = users[msg.sender];
        return u.get_all_projects_name();
    }

    function get_all_commit_logs(uint projectIdx) public only_user view returns(string[] memory){
        project p = users[msg.sender].get_project(projectIdx);
        return p.get_all_commit_logs();
    }

    function new_commit(uint projectIdx , string memory _ipfsHash ,string memory _log) public only_user{
        project p = users[msg.sender].get_project(projectIdx);
        p.new_commit(_ipfsHash,_log);
    }

    function new_comment(uint projectIdx ,uint commitIdx ,string memory _comment) public only_user{
        project p = users[msg.sender].get_project(projectIdx);
        commit c = p.get_commit(commitIdx);
        c.add_comment(users[msg.sender].get_name(),_comment);
    }

    function get_ipfs_hash(uint projectIdx ,uint commitIdx) public view returns(string memory){
        commit c  = users[msg.sender].get_project(projectIdx).get_commit(commitIdx);
        return c.get_ipfs_hash();
    }

    function get_comments(uint projectIdx ,uint commitIdx) public view returns(comment[] memory){
        commit c  = users[msg.sender].get_project(projectIdx).get_commit(commitIdx);
        return c.get_comments();
    }
}