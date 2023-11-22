/* global use, db */

// Select the database to use.
use('AID-Mongo');


// Cuantos documentos tiene la colección personas
db.personas.find({}).count()


// Contenido completo de la colección personas
db.personas.find({})


// Cambiar el DNI de "Milagros Perdomo Gómez" a 1020
db.personas.updateOne(
    { $and: [
        { Nombre: "Milagros" },
        { Apellidos: "Perdomo Gomez" }
    ]},
    { $set: { DNI: 1020 } }
)


// Lista el contenido de la colección personas ordenada de forma ascendente
// por la edad
db.personas.find({}).sort({ Edad: 1 })


// Idem que la anterior pero en formato elegante
db.personas.find({}).pretty().sort({ Edad: 1 })


// Muestra todos los datos de la persona con DNI 3333.
db.personas.find({ DNI: 3333 }, { _id: 0 })


// Muestra el DNI, nombre y apellidos de las personas que vivan en Santa Cruz
db.personas.find(
    {
        Ciudad: "Santa Cruz"
    },
    {
        _id: 0,
        DNI: 1,
        Nombre: 1,
        Apellidos: 1
    }
)


// Muestra el DNI de las personas que viven en Santa Cruz o La Laguna
db.personas.find(
    {
        $or: [
            { Ciudad: "Santa Cruz" },
            { Ciudad: "La Laguna" }
        ]
    },
    {
        _id: 0,
        DNI: 1
    }
)


// Muestra el nombre y apellidos de las personas con edades entre 19 y 25 años
db.personas.find({
    $and: [
        { Edad: { $gte: 19 } },
        { Edad: { $lte: 25 } }
    ]
}).projection({
    _id: 0,
    Nombre: 1,
    Apellidos: 1,
    Edad: 1
})


// Muestra el DNI, nombre y apellidos de las personas a las que les gusta
// el running y la natación.
db.personas.find({
    $and: [
        { Aficiones: { $in: ["running"] } },
        { Aficiones: { $in: ["natacion"] } }
    ]
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// Muestra el DNI, nombre y apellidos de las personas a las que les gusta
// el running o la natación.
db.personas.find({
    Aficiones: { $in: ["running", "natacion"] }
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// Muestra los DNI de las personas que son amigas de la persona con DNI 5555.
db.personas.find({
    Amigos: { $in: [{DNI: 5555}]}
}).projection({
    _id: 0,
    DNI: 1,
    Amigos: 1
})


// Muestra un listado de las aficiones que tienen las personas con edades
// inferiores a 22 años.
