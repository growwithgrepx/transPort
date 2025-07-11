document.addEventListener('DOMContentLoaded', function() {
  document.body.addEventListener('htmx:afterOnLoad', function(evt) {
    try {
      const xhr = evt.detail.xhr;
      if (xhr.responseType === '' && xhr.responseText.trim().startsWith('{')) {
        const data = JSON.parse(xhr.responseText);
        if (data.success && data.id && data.name) {
          // Determine which modal is open
          if (document.getElementById('agentModal') && document.getElementById('agentModal').classList.contains('show')) {
            const select = document.getElementById('agent_id');
            const option = document.createElement('option');
            option.value = data.id;
            option.text = data.name;
            option.selected = true;
            select.appendChild(option);
            const modal = bootstrap.Modal.getInstance(document.getElementById('agentModal'));
            if (modal) modal.hide();
          } else if (document.getElementById('serviceModal') && document.getElementById('serviceModal').classList.contains('show')) {
            const select = document.getElementById('service_id');
            const option = document.createElement('option');
            option.value = data.id;
            option.text = data.name;
            option.selected = true;
            select.appendChild(option);
            const modal = bootstrap.Modal.getInstance(document.getElementById('serviceModal'));
            if (modal) modal.hide();
          } else if (document.getElementById('vehicleModal') && document.getElementById('vehicleModal').classList.contains('show')) {
            const select = document.getElementById('vehicle_id');
            const option = document.createElement('option');
            option.value = data.id;
            option.text = data.name;
            option.selected = true;
            select.appendChild(option);
            const modal = bootstrap.Modal.getInstance(document.getElementById('vehicleModal'));
            if (modal) modal.hide();
          } else if (document.getElementById('driverModal') && document.getElementById('driverModal').classList.contains('show')) {
            const select = document.getElementById('driver_id');
            const option = document.createElement('option');
            option.value = data.id;
            option.text = data.name;
            option.selected = true;
            select.appendChild(option);
            const modal = bootstrap.Modal.getInstance(document.getElementById('driverModal'));
            if (modal) modal.hide();
          }
        }
      }
    } catch (e) { /* ignore */ }
  });
}); 