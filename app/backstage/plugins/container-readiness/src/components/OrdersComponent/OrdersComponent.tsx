import { makeStyles } from '@material-ui/core/styles';
import {
  Table,
  TableColumn,
  Progress,
  ResponseErrorPanel,
} from '@backstage/core-components';
import useAsync from 'react-use/lib/useAsync';
import { useApi, fetchApiRef  } from '@backstage/core-plugin-api';


const useStyles = makeStyles({
  avatar: {
    height: 32,
    width: 32,
    borderRadius: '50%',
  },
});

type Order = {
  order_id: 0,
  app_id: "<none>",
  user_id: "<none>",
  job: {
    form: {
      app_language: "<none>"
    },
    result: -1
  },
  finished: true
};

type DenseTableProps = {
  orders: Order[];
};

export const DenseTable = ({ orders }: DenseTableProps) => {
  
  const classes = useStyles();

  const columns: TableColumn[] = [
    { title: 'Order ID', field: 'order_id' },
    { title: 'App ID', field: 'app_id' },
    { title: 'User ID', field: 'user_id' },
    { title: 'Language', field: 'app_language' },
    { title: 'Status', field: 'finished' },
    { title: 'Result', field: 'result' },
  ];

  const data = orders.map(order => {
    return {
      order_id: order.order_id,
      app_id: order.app_id,
      user_id: order.user_id,
      app_langauge: order.job.form.app_language,
      finished: order.finished,
      result: order.job.result,
    };
  });

  return (
    <Table
      title="Orders"
      options={{ search: false, paging: false }}
      columns={columns}
      data={data}
    />
  );
};

export const OrdersComponent = () => {

  const fetchApi = useApi(fetchApiRef);

  const { value, loading, error } = useAsync(async (): Promise<Order[]> => {
    // go get
    const response = await fetchApi.fetch('/api/cra/order') 
    if (!response.ok) {
      throw new Error("failed to get");
    }
    return response.json()
  }, []);

  if (loading) {
    return <Progress />;
  } else if (error) {
    console.log(error)
    return <ResponseErrorPanel error={error} />;
  }

  return <DenseTable orders={value || []} />;
};
