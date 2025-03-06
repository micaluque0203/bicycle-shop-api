db.createUser({
  user: "admin",
  pwd: "password",
  roles: [
    {
      role: "readWrite",
      db: "marcus_business",
    },
  ],
});

const parts_ids = db.parts.insertMany([
  {
    part_type: "Frame",
    name: "Full-suspension",
    stock_status: "available",
  },
  {
    part_type: "Frame",
    name: "Diamond",
    stock_status: "available",
  },
  {
    part_type: "Wheels",
    name: "Mountain wheels",
    stock_status: "available",
  },
  {
    part_type: "Rim Color",
    name: "Black",
    stock_status: "available",
  },
]);

const config_ids = db.configuration_rules.insertMany([
  {
    depends_on: "wheels",
    depends_value: "mountain wheels",
    forbidden_values: ["diamond", "step-through"],
  },
  {
    depends_on: "wheels",
    depends_value: "fat bike wheels",
    forbidden_values: ["red"],
  },
]);

db.products.insertMany([
  {
    name: "Mountain Bike",
    category: "Bike",
    available_parts: [
      ObjectId("67c490eb10ec1f5ae3491d5a"),
      ObjectId("67c49157780621bd8bc6420e"),
      ObjectId("67c49160780621bd8bc64213"),
      ObjectId("67c491ab1c0e525a32ca5509"),
    ],
    configuration_rules: [
      ObjectId("67c570d4accb9bb94fa00aa1"),
      ObjectId("67c570d4accb9bb94fa00aa2"),
    ],
  },
]);
