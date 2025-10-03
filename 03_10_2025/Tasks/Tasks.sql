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

> db.students.deleteOne({ _id: ObjectId("68dfa4ad6c37f3460a094047") })
{ acknowledged: true, deletedCount: 1 }

> db.Teachers.insertMany([
...   {teacher_id: 1, name: "Rahul", subject: "Math", city: "Mumbai", experience: 5},
...   {teacher_id: 2, name: "Priya", subject: "Science", city: "Delhi", experience: 7},
...   {teacher_id: 3, name: "Arjun", subject: "English", city: "Chennai", experience: 4},
...   {teacher_id: 4, name: "Neha", subject: "History", city: "Bangalore", experience: 6},
...   {teacher_id: 5, name: "Vikram", subject: "Geography", city: "Hyderabad", experience: 3}
... ])
{
  acknowledged: true,
  insertedIds: {
    '0': ObjectId("6522f1e2d1f3a1c1a1a1a1b1"),
    '1': ObjectId("6522f1e2d1f3a1c1a1a1a1b2"),
    '2': ObjectId("6522f1e2d1f3a1c1a1a1a1b3"),
    '3': ObjectId("6522f1e2d1f3a1c1a1a1a1b4"),
    '4': ObjectId("6522f1e2d1f3a1c1a1a1a1b5")
  }
}

> db.Teachers.find()
[
  { _id: ObjectId("..."), teacher_id: 1, name: "Rahul", subject: "Math", city: "Mumbai", experience: 5 },
  { _id: ObjectId("..."), teacher_id: 2, name: "Priya", subject: "Science", city: "Delhi", experience: 7 },
  { _id: ObjectId("..."), teacher_id: 3, name: "Arjun", subject: "English", city: "Chennai", experience: 4 },
  { _id: ObjectId("..."), teacher_id: 4, name: "Neha", subject: "History", city: "Bangalore", experience: 6 },
  { _id: ObjectId("..."), teacher_id: 5, name: "Vikram", subject: "Geography", city: "Hyderabad", experience: 3 }
]

> db.Teachers.find({ city: "Delhi" })
[
  { _id: ObjectId("..."), teacher_id: 2, name: "Priya", subject: "Science", city: "Delhi", experience: 7 }
]

> db.Teachers.find({ experience: { $gt: 5 } })
[
  { _id: ObjectId("..."), teacher_id: 2, name: "Priya", subject: "Science", city: "Delhi", experience: 7 },
  { _id: ObjectId("..."), teacher_id: 4, name: "Neha", subject: "History", city: "Bangalore", experience: 6 }
]

> db.Teachers.updateOne(
...   { teacher_id: 3 },
...   { $set: { experience: 5 } }
... )
{ acknowledged: true, matchedCount: 1, modifiedCount: 1 }

> db.Teachers.updateMany({}, { $set: { email: null } })
{ acknowledged: true, matchedCount: 5, modifiedCount: 5 }

> db.Teachers.deleteOne({ teacher_id: 5 })
{ acknowledged: true, deletedCount: 1 }

> db.Teachers.deleteMany({ city: "Chennai" })
{ acknowledged: true, deletedCount: 1 }