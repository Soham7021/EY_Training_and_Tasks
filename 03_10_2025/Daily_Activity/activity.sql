> db.students.insertMany([
...   {student_id: 1, name: "Rahul", age: 21, city: "Mumbai", course: "AI", marks: 85},
...   {student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "Data Science", marks: 90},
...   {student_id: 3, name: "Arjun", age: 20, city: "Bangalore", course: "Web Development", marks: 78},
...   {student_id: 4, name: "Neha", age: 23, city: "Chennai", course: "Cybersecurity", marks: 88},
...   {student_id: 5, name: "Vikram", age: 21, city: "Hyderabad", course: "Cloud Computing", marks: 82}
... ])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("6522f1e1d1f3a1c1a1a1a1a1"),
    '1': ObjectId("6522f1e1d1f3a1c1a1a1a1a2"),
    '2': ObjectId("6522f1e1d1f3a1c1a1a1a1a3"),
    '3': ObjectId("6522f1e1d1f3a1c1a1a1a1a4"),
    '4': ObjectId("6522f1e1d1f3a1c1a1a1a1a5")
  }
}

> db.students.find()
[
  { _id: ObjectId("..."), student_id: 1, name: "Rahul", age: 21, city: "Mumbai", course: "AI", marks: 85 },
  { _id: ObjectId("..."), student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "Data Science", marks: 90 },
  { _id: ObjectId("..."), student_id: 3, name: "Arjun", age: 20, city: "Bangalore", course: "Web Development", marks: 78 },
  { _id: ObjectId("..."), student_id: 4, name: "Neha", age: 23, city: "Chennai", course: "Cybersecurity", marks: 88 },
  { _id: ObjectId("..."), student_id: 5, name: "Vikram", age: 21, city: "Hyderabad", course: "Cloud Computing", marks: 82 }
]

> db.students.find({ city: "Delhi" })
[
  { _id: ObjectId("..."), student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "Data Science", marks: 90 }
]

> db.students.find({ marks: { $gte: 85 } })
[
  { _id: ObjectId("..."), student_id: 1, name: "Rahul", age: 21, city: "Mumbai", course: "AI", marks: 85 },
  { _id: ObjectId("..."), student_id: 2, name: "Priya", age: 22, city: "Delhi", course: "Data Science", marks: 90 },
  { _id: ObjectId("..."), student_id: 4, name: "Neha", age: 23, city: "Chennai", course: "Cybersecurity", marks: 88 }
]

> db.students.updateOne(
...   { student_id: 3 },
...   { $set: { marks: 80 } }
... )
{ acknowledged: true, matchedCount: 1, modifiedCount: 1 }

> db.students.updateMany({}, { $set: { email: null } })
{ acknowledged: true, matchedCount: 5, modifiedCount: 5 }

> db.students.deleteOne({ student_id: 5 })
{ acknowledged: true, deletedCount: 1 }

> db.students.deleteMany({ city: "Chennai" })
{ acknowledged: true, deletedCount: 1 }
