db = db.getSiblingDB('noc');
db.createUser({
    user: "noc" ,
    pwd: "noc",
    roles: [
        { role:"dbOwner", db: "noc" }
    ]
});
