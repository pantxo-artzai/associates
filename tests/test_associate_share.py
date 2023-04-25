from odoo.tests.common import TransactionCase

class TestAssociateShare(TransactionCase):

    def setUp(self):
        super(TestAssociateShare, self).setUp()
        self.associate = self.env['associates.associate'].create({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'nationality': self.env.ref('base.us').id,
            'partner_id': self.env.ref('base.res_partner_1').id,
            'company_id': self.env.company.id,
            'share_type_id': self.env['associates.share.type'].create({
                'name': 'Test Share Type',
                'description': 'Test share type for unit tests',
                'country_id': self.env.ref('base.us').id,
            }).id
        })

        self.share = self.env['associates.share'].create({
            'associate_id': self.associate.id,
            'value': 100,
            'subscription_date': '2023-01-01',
        })

    def test_create_associate(self):
        self.assertEqual(self.associate.name, 'John Doe')
        self.assertEqual(self.associate.email, 'john.doe@example.com')
        self.assertEqual(self.associate.nationality, self.env.ref('base.us'))

    def test_create_share(self):
        self.assertEqual(self.share.associate_id, self.associate)
        self.assertEqual(self.share.value, 100)
        self.assertEqual(self.share.subscription_date, '2023-01-01')
