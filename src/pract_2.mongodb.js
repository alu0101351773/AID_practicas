/* global use, db */

// Select the database to use.
use('AID-Mongo');

// 1. Cuantos documentos tiene la colección personas
db.personas.find({}).count()


// 2. Contenido completo de la colección personas
db.personas.find({})


// 3. Cambiar el DNI de "Milagros Perdomo Gómez" a 1020
db.personas.updateOne(
    { $and: [
        { Nombre: "Milagros" },
        { Apellidos: "Perdomo Gomez" }
    ]},
    { $set: { DNI: 1020 } }
)


// 4. Lista el contenido de la colección personas ordenada de forma ascendente
// por la edad
db.personas.find({}).sort({ Edad: 1 })


// 5. Idem que la anterior pero en formato elegante
db.personas.find({}).pretty().sort({ Edad: 1 })


// 6. Muestra todos los datos de la persona con DNI 3333.
db.personas.find({ DNI: 3333 }, { _id: 0 })


// 7. Muestra el DNI, nombre y apellidos de las personas que vivan en Santa Cruz
db.personas.find({
    Ciudad: "Santa Cruz"
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// 8. Muestra el DNI de las personas que viven en Santa Cruz o La Laguna
db.personas.find({
    $or: [
        { Ciudad: "Santa Cruz" },
        { Ciudad: "La Laguna" }
    ]
}).projection({
    _id: 0,
    DNI: 1
})


// 9. Muestra el nombre y apellidos de las personas con edades entre 19 y 25 años
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


// 10. Muestra el DNI, nombre y apellidos de las personas a las que les gusta
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


// 11. Muestra el DNI, nombre y apellidos de las personas a las que les gusta
// el running o la natación.
db.personas.find({
    Aficiones: { $in: ["running", "natacion"] }
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// 12. Muestra los DNI de las personas que son amigas de la persona con DNI 5555.
db.personas.find({
    Amigos: { $in: [{DNI: 5555}] }
}).projection({
    _id: 0,
    DNI: 1,
    Amigos: 1
})


// 13. Muestra un listado de las aficiones que tienen las personas con edades
// inferiores a 22 años.
db.personas.find({
    Edad: { $lt: 22 }
}).projection({
    _id: 0,
    Aficiones: 1
})

// Si queremos que lo plasme en un array plano sin repeticiones, podemos añadirle
// el siguiente metodo:
//      .toArray().map(x => x.Aficiones).flat().filter((x, i, a) => a.indexOf(x) === i)


// 14. ¿Cuántas personas viven en Santa Cruz?
db.personas.countDocuments({
    Ciudad: "Santa Cruz"
})


// 15. ¿Cuántos hombres hay en nuestra base de datos?
db.personas.countDocuments({
    Sexo: 'M'
})


// 16. ¿Cuántas personas viven en cada ciudad?
db.personas.aggregate([{
    $group: {
        _id: "$Ciudad",
        Poblacion: {
            $count: {}
        }
    }
}])


// 17. ¿Cuántas personas hay de cada sexo en nuestra base de datos?
db.personas.aggregate([{
    $group: {
        _id: "$Sexo",
        Poblacion: {
            $count: {}
        }
    }
}])


// 18. Muestra para cada persona cuántos amigos tiene
db.personas.aggregate([{
    $project: {
        _id: 0,
        Nombre: 1,
        Apellidos: 1,
        NumAmigos: { $size: "$Amigos" }
    }
}])


// 19. Añade a la lista de aficiones de la persona con DNI 9999 el bricolaje
db.personas.updateOne(
    { DNI: 9999 },
    { $addToSet: { Aficiones: "bricolaje" } }
)

db.personas.find({ DNI: 9999 })


// 20. Incrementa la edad de la persona con DNI 3333 en 2 años
db.personas.updateOne(
    { DNI: 3333 },
    { $inc: { Edad: 2 } }
)


// 21. Muestra los DNI y edades de todos los documentos de la colección personas
db.personas.aggregate([{
    $project: {
        _id: 0,
        DNI: 1,
        Edad: 1
    }
}])


// 22. Modifica los siguientes campos para las personas que vivan en La Laguna:
//     - Multiplica su edad por 2
//     - Añadeles un campo denominado Ocupación con el valor “Estudiante”.
db.personas.updateMany(
    { Ciudad: "La Laguna" },
    {
        $mul: { Edad: 2 },
        $set: { Ocupacion: "Estudiante" }
    }
)


// 23. Muestra todos los datos de las personas que viven en La Laguna
db.personas.find({ Ciudad: "La Laguna" })


// 24. Elimina las personas que vivan en El Sauzal
db.personas.remove({ Ciudad: "El Sauzal" })