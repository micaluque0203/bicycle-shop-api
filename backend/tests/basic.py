# # Unit Tests
# import unittest


# class TestMarcusBusiness(unittest.TestCase):
#     def test_dynamic_configuration_validation(self):
#         rules = [
#             ConfigurationRule("wheels", "mountain wheels", ["diamond", "step-through"]),
#             ConfigurationRule("wheels", "fat bike wheels", ["red"]),
#         ]
#         valid_config = Configuration(
#             {
#                 "frameType": "full-suspension",
#                 "wheels": "mountain wheels",
#                 "rimColor": "black",
#             }
#         )
#         invalid_config = Configuration(
#             {"frameType": "diamond", "wheels": "mountain wheels", "rimColor": "red"}
#         )
#         self.assertTrue(valid_config.is_valid(rules))
#         self.assertFalse(invalid_config.is_valid(rules))

#     def test_order_processing(self):
#         config = Configuration(
#             {
#                 "frameType": "full-suspension",
#                 "wheels": "road wheels",
#                 "rimColor": "blue",
#             }
#         )
#         product = Product("1", "Custom Bicycle", "Bicycles", [], [])
#         order = Order("123", "John Doe")
#         self.assertTrue(order.add_item(config, product))
#         order.fulfill()
#         self.assertEqual(order.status, "fulfilled")

#     def test_invalid_order(self):
#         rules = [ConfigurationRule("wheels", "mountain wheels", ["diamond"])]
#         invalid_config = Configuration(
#             {"frameType": "diamond", "wheels": "mountain wheels"}
#         )
#         product = Product("1", "Custom Bicycle", "Bicycles", [], rules)
#         order = Order("124", "Jane Smith")
#         self.assertFalse(order.add_item(invalid_config, product))


# if __name__ == "__main__":
#     unittest.main()
