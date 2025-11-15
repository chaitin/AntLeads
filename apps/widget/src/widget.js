(function() {
  'use strict';

  // Configuration
  const API_BASE_URL = 'http://10.10.2.229:8001';

  // Get widget ID from script tag
  const currentScript = document.currentScript;
  const WIDGET_ID = currentScript.getAttribute('data-widget-id');

  if (!WIDGET_ID) {
    console.error('AntLeads Widget: Missing data-widget-id attribute');
    return;
  }

  // Widget state
  let config = null;
  let isOpen = false;
  let modalElement = null;
  let buttonElement = null;

  // Load widget configuration
  async function loadConfig() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/widgets/${WIDGET_ID}/config`);
      if (!response.ok) {
        throw new Error(`Failed to load widget config: ${response.status}`);
      }
      config = await response.json();
      return config;
    } catch (error) {
      console.error('AntLeads Widget:', error);
      return null;
    }
  }

  // Create floating button
  function createButton() {
    const button = document.createElement('button');
    button.className = 'antleads-widget-button';
    button.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
    `;

    // Apply positioning
    button.style.cssText = `
      position: fixed;
      z-index: 9998;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: ${config.primary_color};
      color: white;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, box-shadow 0.2s;
    `;

    // Position based on config
    const position = config.button_position || 'bottom-right';
    if (position === 'bottom-right') {
      button.style.bottom = '20px';
      button.style.right = '20px';
    } else if (position === 'bottom-left') {
      button.style.bottom = '20px';
      button.style.left = '20px';
    } else if (position === 'top-right') {
      button.style.top = '20px';
      button.style.right = '20px';
    } else if (position === 'top-left') {
      button.style.top = '20px';
      button.style.left = '20px';
    }

    button.addEventListener('mouseenter', () => {
      button.style.transform = 'scale(1.1)';
      button.style.boxShadow = '0 6px 16px rgba(0,0,0,0.2)';
    });

    button.addEventListener('mouseleave', () => {
      button.style.transform = 'scale(1)';
      button.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
    });

    button.addEventListener('click', () => {
      openModal();
    });

    return button;
  }

  // Create modal
  function createModal() {
    const modal = document.createElement('div');
    modal.className = 'antleads-widget-modal';
    modal.style.cssText = `
      display: none;
      position: fixed;
      z-index: 9999;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      align-items: center;
      justify-content: center;
    `;

    const modalContent = document.createElement('div');
    modalContent.className = 'antleads-widget-modal-content';
    modalContent.style.cssText = `
      background: white;
      border-radius: 8px;
      max-width: 500px;
      width: 90%;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    `;

    // Build form fields
    const fields = config.fields || ['name', 'email', 'phone', 'company', 'estimated_value', 'message'];
    const formFields = fields.map(field => {
      const isTextarea = field === 'message';
      const isRequired = field === 'name' || field === 'email';
      const isNumber = field === 'estimated_value';

      return `
        <div style="margin-bottom: 16px;">
          <label style="display: block; margin-bottom: 8px; font-weight: 500; color: #374151; text-transform: capitalize;">
            ${field.replace('_', ' ')}${isRequired ? ' *' : ''}
          </label>
          ${isTextarea
            ? `<textarea
                 name="${field}"
                 ${isRequired ? 'required' : ''}
                 rows="4"
                 style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; font-family: inherit; resize: vertical;"
                 placeholder="Enter your ${field.replace('_', ' ')}..."></textarea>`
            : isNumber
            ? `<input
                 type="number"
                 name="${field}"
                 ${isRequired ? 'required' : ''}
                 min="0"
                 step="0.01"
                 style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;"
                 placeholder="Enter your ${field.replace('_', ' ')} (e.g., 50000)" />`
            : `<input
                 type="${field === 'email' ? 'email' : field === 'phone' ? 'tel' : 'text'}"
                 name="${field}"
                 ${isRequired ? 'required' : ''}
                 style="width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px;"
                 placeholder="Enter your ${field.replace('_', ' ')}..." />`
          }
        </div>
      `;
    }).join('');

    modalContent.innerHTML = `
      <div style="padding: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <h2 style="margin: 0; font-size: 24px; font-weight: 600; color: #111827;">${config.title}</h2>
          <button type="button" class="antleads-close-button" style="background: none; border: none; font-size: 28px; cursor: pointer; color: #6b7280; line-height: 1; padding: 0; width: 30px; height: 30px;">
            &times;
          </button>
        </div>
        ${config.description ? `<p style="margin-bottom: 20px; color: #6b7280; line-height: 1.6;">${config.description}</p>` : ''}
        <form id="antleads-widget-form">
          ${formFields}
          <div style="margin-top: 24px;">
            <button type="submit" style="width: 100%; padding: 12px; background: ${config.primary_color}; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: 500; cursor: pointer; transition: opacity 0.2s;">
              ${config.submit_button_text || 'Submit'}
            </button>
          </div>
        </form>
        <div id="antleads-success-message" style="display: none; padding: 16px; background: #d1fae5; border-radius: 6px; color: #065f46; margin-top: 16px;">
          ${config.success_message || 'Thank you! We\'ll be in touch soon.'}
        </div>
        <div id="antleads-error-message" style="display: none; padding: 16px; background: #fee2e2; border-radius: 6px; color: #991b1b; margin-top: 16px;"></div>
      </div>
    `;

    modal.appendChild(modalContent);

    // Close button handler
    const closeButton = modalContent.querySelector('.antleads-close-button');
    closeButton.addEventListener('click', closeModal);

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Form submit handler
    const form = modalContent.querySelector('#antleads-widget-form');
    form.addEventListener('submit', handleFormSubmit);

    // Hover effect on submit button
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.addEventListener('mouseenter', () => {
      submitButton.style.opacity = '0.9';
    });
    submitButton.addEventListener('mouseleave', () => {
      submitButton.style.opacity = '1';
    });

    return modal;
  }

  // Handle form submission
  async function handleFormSubmit(e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const data = {
      widget_id: WIDGET_ID,
      name: formData.get('name') || '',
      email: formData.get('email') || null,
      phone: formData.get('phone') || null,
      company: formData.get('company') || null,
      message: formData.get('message') || null,
      estimated_value: formData.get('estimated_value') ? parseFloat(formData.get('estimated_value')) : null,
      url: window.location.href,
      referrer: document.referrer || null
    };

    const successMessage = document.getElementById('antleads-success-message');
    const errorMessage = document.getElementById('antleads-error-message');
    const submitButton = form.querySelector('button[type="submit"]');

    // Reset messages
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';

    // Disable submit button
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/widgets/${WIDGET_ID}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`Submission failed: ${response.status}`);
      }

      const result = await response.json();

      // Show success message
      successMessage.textContent = result.message || config.success_message;
      successMessage.style.display = 'block';

      // Reset form
      form.reset();

      // Close modal after 2 seconds
      setTimeout(() => {
        closeModal();
        successMessage.style.display = 'none';
      }, 2000);

    } catch (error) {
      console.error('AntLeads Widget submission error:', error);
      errorMessage.textContent = 'Something went wrong. Please try again.';
      errorMessage.style.display = 'block';
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = config.submit_button_text || 'Submit';
    }
  }

  // Open modal
  function openModal() {
    if (modalElement) {
      modalElement.style.display = 'flex';
      isOpen = true;
    }
  }

  // Close modal
  function closeModal() {
    if (modalElement) {
      modalElement.style.display = 'none';
      isOpen = false;
      // Reset messages
      const successMessage = document.getElementById('antleads-success-message');
      const errorMessage = document.getElementById('antleads-error-message');
      if (successMessage) successMessage.style.display = 'none';
      if (errorMessage) errorMessage.style.display = 'none';
    }
  }

  // Check if element selector is provided
  function bindToElement() {
    const selector = currentScript.getAttribute('data-bind-to');
    if (selector) {
      const element = document.querySelector(selector);
      if (element) {
        element.addEventListener('click', openModal);
        return true;
      }
    }
    return false;
  }

  // Initialize widget
  async function init() {
    // Load configuration
    config = await loadConfig();
    if (!config) {
      console.error('AntLeads Widget: Failed to load configuration');
      return;
    }

    // Create modal
    modalElement = createModal();
    document.body.appendChild(modalElement);

    // Check if binding to specific element
    const boundToElement = bindToElement();

    // Create floating button if not bound to element
    if (!boundToElement) {
      buttonElement = createButton();
      document.body.appendChild(buttonElement);

      // Auto-open if configured
      if (config.auto_open && config.auto_open_delay) {
        setTimeout(() => {
          openModal();
        }, config.auto_open_delay * 1000);
      }
    }
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose API
  window.AntLeadsWidget = {
    open: openModal,
    close: closeModal,
    isOpen: () => isOpen
  };
})();
