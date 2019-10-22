import { ALERT_TYPES, getBitValue } from './data-types/notifications';

function buildAlertRules( els ) {
  const emptyRule = {
    rule: getBitValue( ALERT_TYPES.NONE ),
    el: null
  };
  const invalidWithTodos = {
    rule: getBitValue( ALERT_TYPES.HAS_TODOS ) | getBitValue( ALERT_TYPES.INVALID ),
    el: els.INCOMPLETE_ALERT
  };
  const oobWithTodos = {
    rule: getBitValue( ALERT_TYPES.HAS_TODOS ) | getBitValue( ALERT_TYPES.OUT_OF_BUDGET ),
    el: els.OOB_W_TODOS
  };
  const inBudgetWithTodos = {
    rule: getBitValue( ALERT_TYPES.HAS_TODOS ) | getBitValue( ALERT_TYPES.IN_BUDGET ),
    el: els.IN_BUDGET_W_TODOS
  };
  const withTodos = {
    rule: getBitValue( ALERT_TYPES.HAS_TODOS ),
    el: els.PENDING_TODOS_ALERT
  };
  const invalid = {
    rule: getBitValue( ALERT_TYPES.INVALID ),
    el: els.INVALID_ALERT
  };
  const inBudget = {
    rule: getBitValue( ALERT_TYPES.IN_BUDGET ),
    el: els.IN_BUDGET_ALERT
  };
  const outOfBudget = {
    rule: getBitValue( ALERT_TYPES.OUT_OF_BUDGET ),
    el: els.OOB_ALERT
  };

  return {
    [emptyRule.rule]: emptyRule.el,
    [invalidWithTodos.rule]: invalidWithTodos.el,
    [oobWithTodos.rule]: oobWithTodos.el,
    [inBudgetWithTodos.rule]: inBudgetWithTodos.el,
    [withTodos.rule]: withTodos.el,
    [invalid.rule]: invalid.el,
    [inBudget.rule]: inBudget.el,
    [outOfBudget.rule]: outOfBudget.el
  };
}

export default buildAlertRules;
