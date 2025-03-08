db = db.getSiblingDB("marcus_business");

db.dropDatabase("marcus_business");

db.users.insertOne({
  email: "admin@test.com",
  hashed_password:
    "$2b$12$TTbnmqv/XBVS5wgKbGgDne96QikbYd0s7irC/UEF.zo8ZrFiplMNW",
  is_active: true,
  is_superuser: true,
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
    part_type: "Rim color",
    name: "Black",
    stock_status: "available",
  },
  {
    part_type: "Chain",
    name: "Single-speed chain",
    stock_status: "available",
  },
  {
    part_type: "Chain",
    name: "8-speed chain",
    stock_status: "out_of_stock",
  },
  {
    part_type: "Rim color",
    name: "Red",
    stock_status: "available",
  },
  {
    part_type: "Rim color",
    name: "Blue",
    stock_status: "available",
  },
]);

const config_ids = db.configuration_rules.insertMany([
  {
    depends_on: "Wheels",
    depends_value: "Mountain wheels",
    forbidden_values: ["Diamond", "Step-through"],
  },
  {
    depends_on: "Wheels",
    depends_value: "Fat bike wheels",
    forbidden_values: ["Red"],
  },
]);

db.products.insertMany([
  {
    name: "Gravel Bike",
    category: "Bike",
    part_ids: Object.values(parts_ids.insertedIds),
    configuration_rule_ids: [],
  },
  {
    name: "Road Bike",
    category: "Bike",
    part_ids: Object.values(parts_ids.insertedIds),
    configuration_rule_ids: [
      config_ids.insertedIds[0],
      config_ids.insertedIds[1],
    ],
  },
  {
    name: "Mountain Bike",
    category: "Bike",
    part_ids: Object.values(parts_ids.insertedIds),
    configuration_rule_ids: [
      config_ids.insertedIds[0],
      config_ids.insertedIds[1],
    ],
  },
]);
