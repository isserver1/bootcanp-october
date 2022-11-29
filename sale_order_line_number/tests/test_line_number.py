from odoo.exceptions import AccessError
from odoo.tests.common import Form, TransactionCase


class TestOrderLine(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestOrderLine, self).setUp(*args, **kwargs)

        # Users
        self.Users = self.env["res.users"].with_context(no_reset_password=True)

        # User Salesman
        self.user_salesman = self.Users.create(
            {
                "name": "Salesman",
                "login": "salesman",
                "groups_id": [(4, self.env.ref("sales_team.group_sale_salesman").id)],
            }
        )

        # User Manager
        self.user_manager = self.Users.create(
            {
                "name": "Manager",
                "login": "manager",
                "groups_id": [(4, self.env.ref("sales_team.group_sale_manager").id)],
            }
        )

        # Create core elements invoked in the tests
        self.customer_bob = self.env["res.partner"].create({"name": "Bob"})
        self.sale_order_1 = self.env["sale.order"].create(
            {"partner_id": self.customer_bob.id}
        )

        self.product_cat = self.env["product.product"].create({"name": "Cat"})

        def validate_much_pepe(self, doge=None):
            if doge == "much":
                return "like"
            return "pepe frog"

        self.env["sale.order.line"]._patch_method(
            "validate_much_doge", validate_much_pepe
        )

    def tearDown(self) -> None:
        super().tearDown()
        self.env["sale.order.line"]._revert_method("validate_much_doge")

    def test_so_line_tag_access(self):
        """Test access to sale order line tags"""

        LineTagSalesman = self.env["sale.order.line.tag"].with_user(self.user_salesman)
        LineTagManager = self.env["sale.order.line.tag"].with_user(self.user_manager)

        tag_salesman = LineTagSalesman.create({"name": "Tag Salesman"})
        tag_manager = LineTagManager.create({"name": "Tag Manager"})

        # Fetch tags as user Salesman
        tag_ids = LineTagSalesman.search(
            [("id", "in", [tag_salesman.id, tag_manager.id])]
        )

        self.assertIn(tag_salesman, tag_ids, "Tag Salesman must be in tags!")
        self.assertEqual(len(tag_ids), 1, "Must be one record only!")

        # Fetch tags as user Manager
        tag_manager_ids = LineTagManager.search(
            [("id", "in", [tag_salesman.id, tag_manager.id])]
        )
        self.assertEqual(len(tag_manager_ids), 2, "Must be two records!")

        # Test Salesman tag write
        with self.assertRaises(AccessError):
            tag_salesman.name = "New Name"

    def test_add_new_line(self):
        """Add new line to SO and check the number"""

        # Add line #1
        with Form(self.sale_order_1) as f:
            with f.order_line.new() as line_1:
                line_1.product_id = self.product_cat
                line_1.sequence = 10
            f.save()

        so_line_1 = self.sale_order_1.order_line[0]

        self.assertEqual(so_line_1.line_number, 1, "Line number must be equal to 1")

        # Add line #2
        with Form(self.sale_order_1) as f:
            with f.order_line.new() as line_2:
                line_2.product_id = self.product_cat
                line_2.sequence = 11
            f.save()

        so_line_2 = self.sale_order_1.order_line[1]

        self.assertEqual(so_line_2.line_number, 2, "Line number must be equal to 2")

        self.sale_order_1.order_line[1].write({"sequence": 6})

        # self.assertEqual(so_line_1.line_number, 2, "Line number must be equal to 2")
        # self.assertEqual(so_line_2.line_number, 1, "Line number must be equal to 1")

        # Delete first line
        so_line_2.unlink()

        self.assertEqual(so_line_1.line_number, 1, "Line number must be equal to 1")

        # Test Doge
        # res = self.env["sale.order.line"].validate_much_doge()
        # self.assertEqual(res, "fun")

        # res2 = self.env["sale.order.line"].validate_much_doge("much")
        # self.assertEqual(res2, "like")
