import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { widgetsApi, Widget, WidgetCreateRequest, WidgetDetail } from '../services/widgets';

const WidgetsPage: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [selectedWidget, setSelectedWidget] = useState<WidgetDetail | null>(null);
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['widgets'],
    queryFn: widgetsApi.list,
  });

  const createMutation = useMutation({
    mutationFn: widgetsApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['widgets'] });
      setSelectedWidget(data);
      setShowModal(false);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: widgetsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['widgets'] });
    },
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const fields = formData.get('fields')?.toString().split(',').map(f => f.trim()) || ['name', 'email', 'phone', 'company', 'estimated_value', 'message'];

    const data: WidgetCreateRequest = {
      name: formData.get('name') as string,
      title: formData.get('title') as string || 'Get in Touch',
      description: formData.get('description') as string || undefined,
      submit_button_text: formData.get('submit_button_text') as string || 'Submit',
      success_message: formData.get('success_message') as string || "Thank you! We'll be in touch soon.",
      fields,
      primary_color: formData.get('primary_color') as string || '#3b82f6',
      button_position: formData.get('button_position') as string || 'bottom-right',
      auto_open: formData.get('auto_open') === 'on',
      auto_open_delay: parseInt(formData.get('auto_open_delay') as string) || 5,
    };

    createMutation.mutate(data);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this widget?')) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Widgets</h1>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Create Widget
        </button>
      </div>

      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {data?.widgets.map((widget: Widget) => (
            <div key={widget.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold mb-1">{widget.name}</h3>
                  <p className="text-sm text-gray-500">{widget.title}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${widget.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                  {widget.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <div className="mb-4">
                <div className="text-xs text-gray-500 mb-1">Widget ID:</div>
                <code className="text-xs bg-gray-100 px-2 py-1 rounded">{widget.widget_id}</code>
              </div>
              <div className="text-xs text-gray-500 mb-4">
                Created: {new Date(widget.created_at).toLocaleDateString()}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    // Show embed code in modal
                    const embedCode = `<script src="http://localhost:8000/static/widget.js" data-widget-id="${widget.widget_id}"></script>`;
                    setSelectedWidget({
                      id: widget.id,
                      name: widget.name,
                      widget_id: widget.widget_id,
                      api_key: '',
                      embed_code: embedCode,
                    });
                  }}
                  className="flex-1 px-3 py-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 text-sm"
                >
                  Get Code
                </button>
                <button
                  onClick={() => handleDelete(widget.id)}
                  className="px-3 py-2 bg-red-50 text-red-700 rounded hover:bg-red-100 text-sm"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Widget Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-90vh overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">Create Widget</h2>
                <button
                  onClick={() => setShowModal(false)}
                  className="modal-close-icon"
                  aria-label="Close modal"
                >
                  ×
                </button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="grid gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Widget Name *</label>
                    <input
                      type="text"
                      name="name"
                      required
                      className="w-full px-3 py-2 border rounded"
                      placeholder="e.g., Homepage Contact Form"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Form Title</label>
                    <input
                      type="text"
                      name="title"
                      className="w-full px-3 py-2 border rounded"
                      defaultValue="Get in Touch"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Description</label>
                    <textarea
                      name="description"
                      rows={3}
                      className="w-full px-3 py-2 border rounded"
                      placeholder="Fill out the form below and we'll get back to you soon."
                    />
                  </div>

  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Submit Button Text</label>
                      <input
                        type="text"
                        name="submit_button_text"
                        className="w-full px-3 py-2 border rounded"
                        defaultValue="Submit"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">Primary Color</label>
                      <input
                        type="color"
                        name="primary_color"
                        className="w-full h-10 px-1 py-1 border rounded"
                        defaultValue="#3b82f6"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Success Message</label>
                    <textarea
                      name="success_message"
                      rows={2}
                      className="w-full px-3 py-2 border rounded"
                      defaultValue="Thank you! We'll be in touch soon."
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Form Fields (comma-separated)</label>
                    <input
                      type="text"
                      name="fields"
                      className="w-full px-3 py-2 border rounded"
                      defaultValue="name,email,phone,company,estimated_value,message"
                      placeholder="name,email,phone,company,estimated_value,message"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Fields visitors will fill out: name, email, phone, company, estimated_value (budget), message
                    </p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Button Position</label>
                    <select
                      name="button_position"
                      className="w-full px-3 py-2 border rounded"
                      defaultValue="bottom-right"
                    >
                      <option value="bottom-right">Bottom Right</option>
                      <option value="bottom-left">Bottom Left</option>
                      <option value="top-right">Top Right</option>
                      <option value="top-left">Top Left</option>
                    </select>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          name="auto_open"
                          className="mr-2"
                        />
                        <span className="text-sm font-medium">Auto-open on page load</span>
                      </label>
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">Auto-open delay (seconds)</label>
                      <input
                        type="number"
                        name="auto_open_delay"
                        className="w-full px-3 py-2 border rounded"
                        defaultValue="5"
                        min="1"
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-6 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 border rounded hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={createMutation.isPending}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                  >
                    {createMutation.isPending ? 'Creating...' : 'Create Widget'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}

      {/* Embed Code Modal */}
      {selectedWidget && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Widget Embed Code</h2>
              <button
                onClick={() => setSelectedWidget(null)}
                className="modal-close-icon"
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                Copy and paste this code into your website's HTML, just before the closing &lt;/body&gt; tag:
              </p>
              <div className="bg-gray-50 p-4 rounded border">
                <code className="text-sm break-all">{selectedWidget.embed_code}</code>
              </div>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(selectedWidget.embed_code);
                  alert('Copied to clipboard!');
                }}
                className="mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                Copy to Clipboard
              </button>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">
                Or bind to a specific element by adding the data-bind-to attribute:
              </p>
              <div className="bg-gray-50 p-4 rounded border">
                <code className="text-sm break-all">
                  {`<script src="http://localhost:8000/static/widget.js" data-widget-id="${selectedWidget.widget_id}" data-bind-to="#my-button"></script>`}
                </code>
              </div>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setSelectedWidget(null)}
                className="px-4 py-2 border rounded hover:bg-gray-50"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WidgetsPage;
