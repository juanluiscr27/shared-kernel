from datetime import UTC, datetime
from uuid import UUID

from sharedkernel.domain.specifications import (
    Condition,
    LogicalOperator,
    Pagination,
    PredicateGroup,
    QuerySpecification,
    SortDirection,
    SortOrder,
)


def test_specification_queries_with_country_equal_do():
    # Arrange
    predicate = Condition.equal(field_name='country', value='DO')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE country = 'DO' LIMIT 50 OFFSET 0"


def test_specification_queries_with_slug_equal_garcia():
    # Arrange
    predicate = Condition.equal(field_name='slug', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE slug = 'garcia' LIMIT 50 OFFSET 0"


def test_specification_queries_with_postal_code_equal_12345():
    # Arrange
    predicate = Condition.equal(field_name='postal_code', value='12345')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE postal_code = '12345' LIMIT 50 OFFSET 0"


def test_specification_queries_with_team_status_equal_active():
    # Arrange
    predicate = Condition.equal(field_name='team_status', value='active')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE team_status = 'active' LIMIT 50 OFFSET 0"


def test_specification_queries_with_active_equal_true():
    # Arrange
    predicate = Condition.equal(field_name='active', value=True)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE active = TRUE LIMIT 50 OFFSET 0"


def test_specification_queries_with_active_equal_false():
    # Arrange
    predicate = Condition.equal(field_name='active', value=False)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE active = FALSE LIMIT 50 OFFSET 0"


def test_specification_queries_with_coach_id_equal_uuid():
    # Arrange
    predicate = Condition.equal(field_name='coach_id', value=UUID('01926a3e-5b7c-7000-8000-000100000000'))
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE coach_id = '01926a3e-5b7c-7000-8000-000100000000' LIMIT 50 OFFSET 0"


def test_specification_queries_with_game_date_equal_datetime():
    # Arrange
    predicate = Condition.equal(field_name='game_date', value=datetime(2024, 6, 15, 19, 0, 0, tzinfo=UTC))
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE game_date = '2024-06-15T19:00:00+00:00' LIMIT 50 OFFSET 0"


def test_specification_queries_with_start_date_equal_date():
    # Arrange
    predicate = Condition.equal(field_name='start_date', value='2024-06-15')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE start_date = '2024-06-15' LIMIT 50 OFFSET 0"


def test_specification_queries_with_start_time_equal_time():
    # Arrange
    predicate = Condition.equal(field_name='start_time', value='19:00:00')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE start_time = '19:00:00' LIMIT 50 OFFSET 0"


def test_specification_queries_with_status_not_equal_inactive():
    # Arrange
    predicate = Condition.not_equal(field_name='status', value='inactive')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE status != 'inactive' LIMIT 50 OFFSET 0"


def test_specification_queries_with_capacity_less_than_5000():
    # Arrange
    predicate = Condition.less_than(field_name='capacity', value=5000)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE capacity < 5000 LIMIT 50 OFFSET 0"


def test_specification_queries_with_weight_less_than_or_equal_95_5():
    # Arrange
    predicate = Condition.less_than_or_equal(field_name='weight', value=95.5)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE weight <= 95.5 LIMIT 50 OFFSET 0"


def test_specification_queries_with_year_greater_than_2020():
    # Arrange
    predicate = Condition.greater_than(field_name='year', value=2020)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE year > 2020 LIMIT 50 OFFSET 0"


def test_specification_queries_with_capacity_greater_than_or_equal_5000():
    # Arrange
    predicate = Condition.greater_than_or_equal(field_name='capacity', value=5000)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE capacity >= 5000 LIMIT 50 OFFSET 0"


def test_specification_queries_with_game_date_greater_than_or_equal_datetime():
    # Arrange
    predicate = Condition.greater_than_or_equal(
        field_name='game_date', value=datetime(2024, 6, 15, 19, 0, 0, tzinfo=UTC),
    )
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE game_date >= '2024-06-15T19:00:00+00:00' LIMIT 50 OFFSET 0"


def test_specification_queries_with_slug_contains_garcia():
    # Arrange
    predicate = Condition.contains(field_name='slug', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE slug LIKE '%garcia%' LIMIT 50 OFFSET 0"


def test_specification_queries_with_first_name_contains_garcia():
    # Arrange
    predicate = Condition.contains(field_name='first_name', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE first_name LIKE '%garcia%' LIMIT 50 OFFSET 0"


def test_specification_queries_with_slug_not_contains_test():
    # Arrange
    predicate = Condition.not_contains(field_name='slug', value='test')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE slug NOT LIKE '%test%' LIMIT 50 OFFSET 0"


def test_specification_queries_with_slug_starts_with_garcia():
    # Arrange
    predicate = Condition.starts_with(field_name='slug', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE slug LIKE 'garcia%' LIMIT 50 OFFSET 0"


def test_specification_queries_with_slug_ends_with_jr():
    # Arrange
    predicate = Condition.ends_with(field_name='slug', value='jr')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE slug LIKE '%jr' LIMIT 50 OFFSET 0"


def test_specification_queries_with_game_date_between_datetime_ranges():
    # Arrange
    predicate = Condition.between(
        field_name='game_date',
        left=datetime(2024, 6, 15, 19, 0, 0, tzinfo=UTC),
        right=datetime(2024, 6, 30, 21, 0, 0, tzinfo=UTC),
    )
    pagination = Pagination()
    expected = "WHERE game_date BETWEEN '2024-06-15T19:00:00+00:00' AND '2024-06-30T21:00:00+00:00' LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == expected


def test_specification_queries_with_year_between_2024_and_2026():
    # Arrange
    predicate = Condition.between(field_name='year', left=2024, right=2026)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE year BETWEEN 2024 AND 2026 LIMIT 50 OFFSET 0"


def test_specification_queries_with_country_in_do_us_pr():
    # Arrange
    predicate = Condition.is_in(field_name='country', values=['DO', 'US', 'PR'])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE country IN ('DO', 'US', 'PR') LIMIT 50 OFFSET 0"


def test_specification_queries_with_description_is_null():
    # Arrange
    predicate = Condition.is_null(field_name='description')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE description IS NULL LIMIT 50 OFFSET 0"


def test_specification_queries_with_headshot_url_is_null():
    # Arrange
    predicate = Condition.is_null(field_name='headshot_url')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE headshot_url IS NULL LIMIT 50 OFFSET 0"


def test_specification_queries_with_description_is_not_null():
    # Arrange
    predicate = Condition.is_not_null(field_name='description')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE description IS NOT NULL LIMIT 50 OFFSET 0"


def test_specification_queries_with_headshot_url_is_not_null():
    # Arrange
    predicate = Condition.is_not_null(field_name='headshot_url')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE headshot_url IS NOT NULL LIMIT 50 OFFSET 0"


def test_specification_queries_with_country_do_and_sex_male_and_status_active():
    # Arrange
    predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.equal(field_name='country', value='DO'),
        Condition.equal(field_name='sex', value='male'),
        Condition.equal(field_name='status', value='active'),
    ])
    pagination = Pagination()
    expected = "WHERE country = 'DO' AND sex = 'male' AND status = 'active' LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == expected


def test_specification_queries_with_last_name_contains_garcia_and_country_do():
    # Arrange
    predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.contains(field_name='last_name', value='garcia'),
        Condition.equal(field_name='country', value='DO'),
    ])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE last_name LIKE '%garcia%' AND country = 'DO' LIMIT 50 OFFSET 0"


def test_specification_queries_with_pts_gt_20_and_ast_gt_10():
    # Arrange
    predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.greater_than(field_name='pts', value=20),
        Condition.greater_than(field_name='ast', value=10),
    ])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE pts > 20 AND ast > 10 LIMIT 50 OFFSET 0"


def test_specification_queries_with_position_pg_or_pts_gt_20_and_ast_gt_10():
    # Arrange
    expression1 = PredicateGroup(operator=LogicalOperator.OR, predicates=[
        Condition.equal(field_name='position', value='PG'),
    ])
    expression2 = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.greater_than(field_name='pts', value=20),
        Condition.greater_than(field_name='ast', value=10),
    ])
    predicate = expression1 | expression2
    pagination = Pagination()
    expected = "WHERE (position = 'PG') OR (pts > 20 AND ast > 10) LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == expected


def test_specification_queries_with_position_sg_and_pts_gt_20_or_ast_gt_10():
    # Arrange
    expression1 = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.equal(field_name='position', value='SG'),
    ])
    expression2 = PredicateGroup(operator=LogicalOperator.OR, predicates=[
        Condition.greater_than(field_name='pts', value=20),
        Condition.greater_than(field_name='ast', value=10),
    ])
    predicate = expression1 & expression2
    pagination = Pagination()
    expected = "WHERE (position = 'SG') AND (pts > 20 OR ast > 10) LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == expected


def test_specification_queries_ordered_by_last_name_asc():
    # Arrange
    sorting = [SortOrder(field_name='last_name', direction=SortDirection.ASC)]
    pagination = Pagination()

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "ORDER BY last_name ASC LIMIT 50 OFFSET 0"


def test_specification_queries_ordered_by_last_name_desc():
    # Arrange
    sorting = [SortOrder(field_name='last_name', direction=SortDirection.DESC)]
    pagination = Pagination()

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "ORDER BY last_name DESC LIMIT 50 OFFSET 0"


def test_specification_queries_ordered_by_last_name_asc_and_first_name_desc():
    # Arrange
    sorting = [
        SortOrder(field_name='last_name', direction=SortDirection.ASC),
        SortOrder(field_name='first_name', direction=SortDirection.DESC),
    ]
    pagination = Pagination()

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "ORDER BY last_name ASC, first_name DESC LIMIT 50 OFFSET 0"


def test_specification_queries_ordered_by_last_name_desc_and_first_name_desc():
    # Arrange
    sorting = [
        SortOrder(field_name='last_name', direction=SortDirection.DESC),
        SortOrder(field_name='first_name', direction=SortDirection.DESC),
    ]
    pagination = Pagination()

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "ORDER BY last_name DESC, first_name DESC LIMIT 50 OFFSET 0"


def test_specification_queries_ordered_by_last_name_asc_and_year_desc():
    # Arrange
    sorting = [
        SortOrder(field_name='last_name', direction=SortDirection.ASC),
        SortOrder(field_name='year', direction=SortDirection.DESC),
    ]
    pagination = Pagination()

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "ORDER BY last_name ASC, year DESC LIMIT 50 OFFSET 0"


def test_specification_queries_ordered_by_last_name_desc_and_first_name_asc_and_year_asc():
    # Arrange
    sorting = [
        SortOrder(field_name='last_name', direction=SortDirection.DESC),
        SortOrder(field_name='first_name', direction=SortDirection.ASC),
        SortOrder(field_name='year', direction=SortDirection.ASC),
    ]
    pagination = Pagination()
    expected = "ORDER BY last_name DESC, first_name ASC, year ASC LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == expected


def test_specification_queries_with_limit_10_offset_0():
    # Arrange
    pagination = Pagination(limit=10, offset=0)

    # Act
    specification = QuerySpecification(pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "LIMIT 10 OFFSET 0"


def test_specification_queries_with_limit_25_offset_10():
    # Arrange
    pagination = Pagination(limit=25, offset=10)

    # Act
    specification = QuerySpecification(pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "LIMIT 25 OFFSET 10"


def test_specification_queries_with_limit_50_offset_0():
    # Arrange
    pagination = Pagination(limit=50, offset=0)

    # Act
    specification = QuerySpecification(pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "LIMIT 50 OFFSET 0"


def test_specification_queries_with_country_do_ordered_by_last_name_asc_limit_10_offset_0():
    # Arrange
    predicate = Condition.equal(field_name='country', value='DO')
    sorting = [SortOrder(field_name='last_name', direction=SortDirection.ASC)]
    pagination = Pagination(limit=10, offset=0)

    # Act
    specification = QuerySpecification(predicate=predicate, sorting=sorting, pagination=pagination)
    result = specification.to_expression()

    # Assert
    assert result == "WHERE country = 'DO' ORDER BY last_name ASC LIMIT 10 OFFSET 0"


def test_specification_template_with_country_equal_do():
    # Arrange
    predicate = Condition.equal(field_name='country', value='DO')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE country = %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'DO'}


def test_specification_template_with_active_equal_true():
    # Arrange
    predicate = Condition.equal(field_name='active', value=True)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE active = %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': True}


def test_specification_template_with_status_not_equal_inactive():
    # Arrange
    predicate = Condition.not_equal(field_name='status', value='inactive')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE status != %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'inactive'}


def test_specification_template_with_capacity_less_than_5000():
    # Arrange
    predicate = Condition.less_than(field_name='capacity', value=5000)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE capacity < %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 5000}


def test_specification_template_with_weight_less_than_or_equal_95_5():
    # Arrange
    predicate = Condition.less_than_or_equal(field_name='weight', value=95.5)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE weight <= %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 95.5}


def test_specification_template_with_year_greater_than_2020():
    # Arrange
    predicate = Condition.greater_than(field_name='year', value=2020)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE year > %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 2020}


def test_specification_template_with_capacity_greater_than_or_equal_5000():
    # Arrange
    predicate = Condition.greater_than_or_equal(field_name='capacity', value=5000)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE capacity >= %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 5000}


def test_specification_template_with_coach_id_equal_uuid():
    # Arrange
    predicate = Condition.equal(field_name='coach_id', value=UUID('01926a3e-5b7c-7000-8000-000100000000'))
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE coach_id = %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': UUID('01926a3e-5b7c-7000-8000-000100000000')}


def test_specification_template_with_game_date_equal_datetime():
    # Arrange
    predicate = Condition.equal(field_name='game_date', value=datetime(2024, 6, 15, 19, 0, 0, tzinfo=UTC))
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE game_date = %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': datetime(2024, 6, 15, 19, 0, 0, tzinfo=UTC)}


def test_specification_template_with_country_in_do_us_pr():
    # Arrange
    predicate = Condition.is_in(field_name='country', values=['DO', 'US', 'PR'])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE country IN (%(p0)s, %(p1)s, %(p2)s) LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'DO', 'p1': 'US', 'p2': 'PR'}


def test_specification_template_with_status_not_in_inactive_archived():
    # Arrange
    predicate = Condition.not_in(field_name='status', values=['inactive', 'archived'])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE status NOT IN (%(p0)s, %(p1)s) LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'inactive', 'p1': 'archived'}


def test_specification_template_with_year_between_2024_and_2026():
    # Arrange
    predicate = Condition.between(field_name='year', left=2024, right=2026)
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE year BETWEEN %(p0)s AND %(p1)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 2024, 'p1': 2026}


def test_specification_template_with_slug_contains_garcia():
    # Arrange
    predicate = Condition.contains(field_name='slug', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE slug LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%garcia%'}


def test_specification_template_with_slug_not_contains_test():
    # Arrange
    predicate = Condition.not_contains(field_name='slug', value='test')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE slug NOT LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%test%'}


def test_specification_template_with_slug_starts_with_garcia():
    # Arrange
    predicate = Condition.starts_with(field_name='slug', value='garcia')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE slug LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'garcia%'}


def test_specification_template_with_slug_ends_with_jr():
    # Arrange
    predicate = Condition.ends_with(field_name='slug', value='jr')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE slug LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%jr'}


def test_specification_template_with_label_contains_100_percent():
    # Arrange
    predicate = Condition.contains(field_name='label', value='100%')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE label LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%100\\%%'}


def test_specification_template_with_name_contains_under_score():
    # Arrange
    predicate = Condition.contains(field_name='name', value='user_name')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE name LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%user\\_name%'}


def test_specification_template_with_label_starts_with_50_percent_off():
    # Arrange
    predicate = Condition.starts_with(field_name='label', value='50% off')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE label LIKE %(p0)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '50\\% off%'}


def test_specification_template_with_description_is_null():
    # Arrange
    predicate = Condition.is_null(field_name='description')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE description IS NULL LIMIT 50 OFFSET 0"
    assert parameters == {}


def test_specification_template_with_headshot_url_is_not_null():
    # Arrange
    predicate = Condition.is_not_null(field_name='headshot_url')
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE headshot_url IS NOT NULL LIMIT 50 OFFSET 0"
    assert parameters == {}


def test_specification_template_with_country_do_and_sex_male_and_status_active():
    # Arrange
    predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.equal(field_name='country', value='DO'),
        Condition.equal(field_name='sex', value='male'),
        Condition.equal(field_name='status', value='active'),
    ])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE country = %(p0)s AND sex = %(p1)s AND status = %(p2)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': 'DO', 'p1': 'male', 'p2': 'active'}


def test_specification_template_with_last_name_contains_garcia_and_country_do():
    # Arrange
    predicate = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.contains(field_name='last_name', value='garcia'),
        Condition.equal(field_name='country', value='DO'),
    ])
    pagination = Pagination()

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE last_name LIKE %(p0)s AND country = %(p1)s LIMIT 50 OFFSET 0"
    assert parameters == {'p0': '%garcia%', 'p1': 'DO'}


def test_specification_template_with_position_pg_or_pts_gt_20_and_ast_gt_10():
    # Arrange
    expression1 = PredicateGroup(operator=LogicalOperator.OR, predicates=[
        Condition.equal(field_name='position', value='PG'),
    ])
    expression2 = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.greater_than(field_name='pts', value=20),
        Condition.greater_than(field_name='ast', value=10),
    ])
    predicate = expression1 | expression2
    pagination = Pagination()
    expected = "WHERE (position = %(p0)s) OR (pts > %(p1)s AND ast > %(p2)s) LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == expected
    assert parameters == {'p0': 'PG', 'p1': 20, 'p2': 10}


def test_specification_template_with_position_sg_and_pts_gt_20_or_ast_gt_10():
    # Arrange
    expression1 = PredicateGroup(operator=LogicalOperator.AND, predicates=[
        Condition.equal(field_name='position', value='SG'),
    ])
    expression2 = PredicateGroup(operator=LogicalOperator.OR, predicates=[
        Condition.greater_than(field_name='pts', value=20),
        Condition.greater_than(field_name='ast', value=10),
    ])
    predicate = expression1 & expression2
    pagination = Pagination()
    expected = "WHERE (position = %(p0)s) AND (pts > %(p1)s OR ast > %(p2)s) LIMIT 50 OFFSET 0"

    # Act
    specification = QuerySpecification(predicate=predicate, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == expected
    assert parameters == {'p0': 'SG', 'p1': 20, 'p2': 10}


def test_specification_template_with_country_do_ordered_by_last_name_asc_limit_10_offset_0():
    # Arrange
    predicate = Condition.equal(field_name='country', value='DO')
    sorting = [SortOrder(field_name='last_name', direction=SortDirection.ASC)]
    pagination = Pagination(limit=10, offset=0)

    # Act
    specification = QuerySpecification(predicate=predicate, sorting=sorting, pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "WHERE country = %(p0)s ORDER BY last_name ASC LIMIT 10 OFFSET 0"
    assert parameters == {'p0': 'DO'}


def test_specification_template_with_no_predicate_limit_25_offset_10():
    # Arrange
    pagination = Pagination(limit=25, offset=10)

    # Act
    specification = QuerySpecification(pagination=pagination)
    template = specification.to_template()
    parameters = specification.parameters

    # Assert
    assert template == "LIMIT 25 OFFSET 10"
    assert parameters == {}


def test_specification_limit_delegates_to_pagination():
    # Arrange
    pagination = Pagination(limit=10, offset=5)

    # Act
    specification = QuerySpecification(pagination=pagination)

    # Assert
    assert specification.limit == 10


def test_specification_offset_delegates_to_pagination():
    # Arrange
    pagination = Pagination(limit=10, offset=5)

    # Act
    specification = QuerySpecification(pagination=pagination)

    # Assert
    assert specification.offset == 5
