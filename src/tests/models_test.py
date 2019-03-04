from src.models import Company


def test_create_company(session):
    company = Company(
        name='Code Fellows',
        symbol='CF',
        exchange='Some Exchange',
        description='We learn more faster'
    )
    session.add(company)
    session.commit()
    assert company.id > 0
    companies = Company.query.all()
    assert len(companies) == 1
    assert companies[0].name == 'Code Fellows'
    assert companies[0].symbol == 'CF'
