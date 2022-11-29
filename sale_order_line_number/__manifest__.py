# Copyright Cetmix OU
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Line Number",
    "summary": "Line numbers in Sales Order lines",
    "version": "14.0.0.0.1",
    "category": "Sales",
    "website": "https://github.com/isserver1/bootcanp-october",
    "author": "Cetmix Bootcamp",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_line.xml",
    ],
    "demo": [
        "data/demo_data.xml",
    ],
}
