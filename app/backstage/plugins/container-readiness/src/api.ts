import { createApiRef, DiscoveryApi, FetchApi } from '@backstage/core-plugin-api';

export interface Order {
    order_id: string;
    app_id: string;
    user_id: string;
    job: {
        order_id: string;
        current_step: number;
        form: {
            user_id: string;
            app_id: string;
            app_language: string;
            config_text: string;            
        },
        result: number;
    },
    finished: boolean;    
}

export interface OrderApi {
    url: string;
    getOrders: () => Promise<List<Order>>;
    getOrder: (orderId: string) => Promise<Order>;
}

export const OrderApiRef = createApiRef<OrderApi>({
    id: 'plugin.container-readiness.service',
});

export class OrderApiClient implements OrderApiRef {
    discoveryApi: DiscoveryApi;
    fetchApi: FetchApi;

    constructor({discoveryApi,fetchApi}: {discoveryApi: DiscoveryApi, fetchApi: FetchApi}) {
        this.discoveryApi = discoveryApi;
        this.fetchApi = fetchApi;
    }

    private async fetch<T = any>(input: string, init?: RequestInit): Promise<T> {
        const proxyUri = `${await this.discoveryApi.getBaseUrl('proxy')}/container-readiness-api`;

        const response = await this.fetchApi.fetch(`${proxyUri}${input}`, init);
        if (!response.ok) throw new Error(response.statusText);
        return await response.json()
    }

    async getOrders(): Promise<List<Order>> {
        return await this.fetch<List<Order>>('/orders');
    }

    async getOrder(orderId: string): Promise<Order> {
        return await this.fetch<Order>(`/order/${orderId}`);
    }
}

