/* global use, db */

// Select the database to use.
use('AID-Mongo');

// 1. Cuantos documentos tiene la colección personas
use('AID-Mongo');
db.personas.find({}).count()


// 2. Contenido completo de la colección personas
use('AID-Mongo');
db.personas.find({})


// 3. Cambiar el DNI de "Milagros Perdomo Gómez" a 1020
use('AID-Mongo');
db.personas.updateOne(
    { 
        $and: [
            { Nombre: "Milagros" },
            { Apellidos: "Perdomo Gomez" }
        ]
    },
    {
        $set: {
            DNI: 1020
        }
    }
)

db.personas.find({DNI: 1020})


// 4. Lista el contenido de la colección personas ordenada de forma ascendente
// por la edad
use('AID-Mongo');
db.personas.find({}).sort({ Edad: 1 })


// 5. Idem que la anterior pero en formato elegante
use('AID-Mongo');
db.personas.find({}).pretty().sort({ Edad: 1 })


// 6. Muestra todos los datos de la persona con DNI 3333.
use('AID-Mongo');
db.personas.find({
    DNI: 3333
}).projection({
    _id: 0
})


// 7. Muestra el DNI, nombre y apellidos de las personas que vivan en Santa Cruz
use('AID-Mongo');
db.personas.find({
    Ciudad: "Santa Cruz"
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// 8. Muestra el DNI de las personas que viven en Santa Cruz o La Laguna
use('AID-Mongo');
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
use('AID-Mongo');
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
use('AID-Mongo');
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
use('AID-Mongo');
db.personas.find({
    Aficiones: { $in: ["running", "natacion"] }
}).projection({
    _id: 0,
    DNI: 1,
    Nombre: 1,
    Apellidos: 1
})


// 12. Muestra los DNI de las personas que son amigas de la persona con DNI 5555.
use('AID-Mongo');
db.personas.find({
    Amigos: { $in: [{DNI: 5555}] }
}).projection({
    _id: 0,
    DNI: 1
})


// 13. Muestra un listado de las aficiones que tienen las personas con edades
// inferiores a 22 años.
use('AID-Mongo');
db.personas.find({
    Edad: { $lt: 22 }
}).projection({
    _id: 0,
    Aficiones: 1
})


// 14. ¿Cuántas personas viven en Santa Cruz?
use('AID-Mongo');
db.personas.countDocuments({
    Ciudad: "Santa Cruz"
})


// 15. ¿Cuántos hombres hay en nuestra base de datos?
use('AID-Mongo');
db.personas.countDocuments({
    Sexo: 'H'
})


// 16. ¿Cuántas personas viven en cada ciudad?
use('AID-Mongo');
db.personas.aggregate([{
    $group: {
        _id: "$Ciudad",
        Poblacion: {
            $count: {}
        }
    }
}])


// 17. ¿Cuántas personas hay de cada sexo en nuestra base de datos?
use('AID-Mongo');
db.personas.aggregate([{
    $group: {
        _id: "$Sexo",
        Poblacion: {
            $count: {}
        }
    }
}])


// 18. Muestra para cada persona cuántos amigos tiene
use('AID-Mongo');
db.personas.aggregate([{
    $project: {
        _id: 0,
        Nombre: 1,
        Apellidos: 1,
        NumAmigos: { $size: "$Amigos" }
    }
}])


// 19. Añade a la lista de aficiones de la persona con DNI 9999 el bricolaje
use('AID-Mongo');
db.personas.updateOne(
    { DNI: 9999 },
    { $addToSet: { Aficiones: "bricolaje" } }
)
db.personas.find({DNI: 9999})


// 20. Incrementa la edad de la persona con DNI 3333 en 2 años
use('AID-Mongo');
db.personas.updateOne(
    { DNI: 3333 },
    { $inc: { Edad: 2 } }
)
db.personas.find({DNI: 3333})

// 21. Muestra los DNI y edades de todos los documentos de la colección personas
use('AID-Mongo');
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
use('AID-Mongo');
db.personas.updateMany(
    { Ciudad: "La Laguna" },
    {
        $mul: { Edad: 2 },
        $set: { Ocupacion: "Estudiante" }
    }
)


// 23. Muestra todos los datos de las personas que viven en La Laguna
use('AID-Mongo');
db.personas.find({ Ciudad: "La Laguna" })


// 24. Elimina las personas que vivan en El Sauzal
use('AID-Mongo');
db.personas.deleteMany({ Ciudad: "El Sauzal" })
// db.personas.find({ Ciudad: "El Sauzal"})

// 25. Muestra el contenido de la colección personas ordenado de forma
// descendente por ciudad
use('AID-Mongo');
db.personas.aggregate([{
    $project: {
        _id: 0,
        Aficiones: 1,
        Amigos: 1,
        Apellidos: 1,
        Ciudad: 1,
        DNI: 1,
        Edad: 1,
        Nombre: 1,
        Ocupacion: 1,
        Sexo: 1        
    }
}]).sort({ Ciudad: -1 })


// 26. Elimina las personas que tengan un solo amigo
use('AID-Mongo');
db.personas.deleteMany({
    Amigos: { $size: 1 }  
})


// 27. Muestra el contenido de la colección personas ordenado de forma
// descendente por ciudad y ascendente por los campos apellidos y nombre
use('AID-Mongo');
db.personas.aggregate([{
    $project: {
        _id: 0,
        Aficiones: 1,
        Amigos: 1,
        Apellidos: 1,
        Ciudad: 1,
        DNI: 1,
        Edad: 1,
        Nombre: 1,
        Ocupacion: 1,
        Sexo: 1
    }
}]).sort({
    Ciudad: -1,
    Apellidos: 1,
    Nombre: 1
})


// 28. DNI de las personas que tienen al menos un amigo en la misma ciudad
// en que viven


// 29. DNI de las personas que tienen algún amigo que comparta con ellos
// alguna afición


// 30. Muestra los DNI de las personas que tienen amigos en común