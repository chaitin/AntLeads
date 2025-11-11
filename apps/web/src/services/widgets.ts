import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Widget {
  id: string;
  name: string;
  widget_id: string;
  title: string;
  is_active: boolean;
  created_at: string;
}

export interface WidgetDetail {
  id: string;
  widget_id: string;
  api_key: string;
  name: string;
  embed_code: string;
}

export interface WidgetCreateRequest {
  name: string;
  title?: string;
  description?: string;
  submit_button_text?: string;
  success_message?: string;
  fields?: string[];
  primary_color?: string;
  button_position?: string;
  auto_open?: boolean;
  auto_open_delay?: number;
}

export interface WidgetUpdateRequest {
  name?: string;
  title?: string;
  description?: string;
  submit_button_text?: string;
  success_message?: string;
  fields?: string[];
  primary_color?: string;
  button_position?: string;
  auto_open?: boolean;
  auto_open_delay?: number;
  is_active?: boolean;
}

export const widgetsApi = {
  async list() {
    const { data } = await api.get<{ widgets: Widget[] }>('/widgets/');
    return data;
  },

  async create(data: WidgetCreateRequest) {
    const { data: response } = await api.post<WidgetDetail>('/widgets/', data);
    return response;
  },

  async update(id: string, data: WidgetUpdateRequest) {
    const { data: response } = await api.patch(`/widgets/${id}`, data);
    return response;
  },

  async delete(id: string) {
    await api.delete(`/widgets/${id}`);
  },
};
