import {
  Table,
  TableColumn,
  ResponseErrorPanel,
  Progress,
} from '@backstage/core-components';
import { useState, useEffect } from 'react';
import { OrderApiRef } from '../../api';
import { useApi, useRouteRef } from '@backstage/core-plugin-api';

import { orderRouteRef } from '../../routes';


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

  const getOrderPath = useRouteRef(orderRouteRef);

  const columns: TableColumn[] = [
    { title: 'Order ID', field: 'order_id', render: (rowData) => (
      <a href={getOrderPath() + '/' + rowData.order_id} rel="noopener noreferrer">
        {rowData.order_id}
      </a>
    ) },
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

  const apiClient = useApi(OrderApiRef);

  const { refreshKey } = useRefresh();

  const [orders, setOrders] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const fetchedOrders = await apiClient.getOrders();
        setOrders(fetchedOrders || []);
      } catch (err) {
        setError(err);
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [apiClient,refreshKey]);

  if (loading) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error}/>
  } else {
    return <DenseTable orders={orders || []}  />;
  }
};
