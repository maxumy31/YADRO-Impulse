const endpoint = "https://dummyjson.com/users";

export async function deleteUser(id) {
    return await fetch(`${endpoint}/${id}`, { method: "DELETE" });
}

export async function getUsers(page = 1, pageSize = 30, search = "") {
    return await fetch(`${endpoint}/search?q=${search}&skip=${(page - 1) * pageSize}&limit=${pageSize}`)
        .then(res => res.json())
        .then(json => {
            return {
                total : json.total,
                users: json.users.map(user => {
                    return {
                        name: `${user.firstName} ${user.lastName}`,
                        email: user.email,
                        phone: [...user.phone].filter(c => /\d/.test(c)).join(''),
                        id: user.id,
                    };
                })
            }
        })
}

export async function createUser(user) {
    return await fetch(`${endpoint}/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: user.name,
            email: user.email,
            id: user.id,
            phone: user.id,
        })
    })
}