from todo.utils import dev_secrets

connection_config = {
  'user': dev_secrets.USER,
  'password': dev_secrets.PASSWORD,
  'host': dev_secrets.HOST,
  'database': dev_secrets.DATABASE,
  'raise_on_warnings': True
}
