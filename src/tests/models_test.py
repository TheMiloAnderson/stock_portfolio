from src.models import Company, Portfolio, User


class TestCompanyModel():

    def test_create_co(self, company):
        assert company

    def test_co_data(self, company):
        assert company.name == 'Code Fellows'
        assert company.symbol == 'CF'
        assert company.exchange == 'Some Exchange'
        assert company.description == 'We learn more faster'

    def test_co_query(self, company):
        companies = Company.query.all()
        assert len(companies) == 1


class TestPortfolioModel():

    def test_create_portfolio(self, portfolio):
        assert portfolio.id > 0

    def test_portfolio_data(self, portfolio):
        assert portfolio.name == 'test_portfolio'

    def test_portfolio_query(self, portfolio):
        portfolios = Portfolio.query.all()
        assert len(portfolios) == 1


class TestCompanyPortfolioRelationship():

    def test_co_has_port(self):
        red = Portfolio(name='red')
        cf = Company(
            name='Code Fellows',
            symbol='CF',
            exchange='Some Exchange',
            description='We learn more faster',
            portfolio=red
        )
        assert cf.portfolio.name == 'red'

    def test_port_has_co(self):
        blue = Portfolio(name='blue')
        cf = Company(
            name='Code Fellows',
            symbol='CF',
            exchange='Some Exchange',
            description='We learn more faster',
            portfolio=blue
        )
        fc = Company(
            name='Mirror Universe Code Fellows',
            symbol='FC',
            exchange='Exchange Some',
            description='We forget less slower',
            portfolio=blue
        )
        assert blue.companies[0].symbol == 'CF'
        assert blue.companies[1].symbol == 'FC'


class TestUserModel():

    def test_create_user(self, user):
        assert user

    def test_user_data(self, user):
        assert user.email == 'test@pytest.com'
        assert user.password
