// Chat Window Functionality
class FleetChat {
  constructor() {
    this.chatWindow = document.getElementById('chat-window');
    this.chatToggle = document.getElementById('chatToggle');
    this.chatMessages = document.getElementById('chatMessages');
    this.downloadSection = document.getElementById('downloadSection');
    this.downloadBtn = document.getElementById('downloadBtn');
    
    // Control buttons
    this.dockBtn = document.getElementById('dockBtn');
    this.minimizeBtn = document.getElementById('minimizeBtn');
    this.fullscreenBtn = document.getElementById('fullscreenBtn');
    this.closeBtn = document.getElementById('closeBtn');
    
    this.isMinimized = false;
    this.isFullscreen = false;
    this.isDocked = false;
    this.isHidden = false;
    this.currentData = null;
    this.currentQuery = null;
    
    this.init();
  }
  
  init() {
    this.restoreState();
    this.bindEvents();
    this.showChatToggle();
  }
  
  restoreState() {
    // Restore chat window state from localStorage
    const savedState = localStorage.getItem('chatWindowState');
    if (savedState) {
      const state = JSON.parse(savedState);
      this.isMinimized = state.isMinimized || false;
      this.isFullscreen = state.isFullscreen || false;
      this.isDocked = state.isDocked || false;
      this.isHidden = state.isHidden || false;
      
      // Apply saved state
      if (this.isHidden) {
        this.chatWindow.style.display = 'none';
        this.showChatToggle();
      } else {
        this.chatWindow.style.display = 'flex';
        this.chatToggle.style.display = 'none';
      }
      
      if (this.isMinimized) {
        this.chatWindow.classList.add('minimized');
        this.chatMessages.style.display = 'none';
        document.querySelector('.chat-buttons-container').style.display = 'none';
        this.downloadSection.style.display = 'none';
      }
      
      if (this.isFullscreen) {
        this.chatWindow.classList.add('fullscreen');
        this.chatWindow.style.width = 'auto';
        this.chatWindow.style.height = 'auto';
      }
      
      if (this.isDocked) {
        this.chatWindow.classList.add('docked');
      }
    }
  }
  
  saveState() {
    // Save current state to localStorage
    const state = {
      isMinimized: this.isMinimized,
      isFullscreen: this.isFullscreen,
      isDocked: this.isDocked,
      isHidden: this.isHidden
    };
    localStorage.setItem('chatWindowState', JSON.stringify(state));
  }
  
  bindEvents() {
    // Toggle chat window
    this.chatToggle.addEventListener('click', () => this.toggleChat());
    
    // Control buttons
    this.dockBtn.addEventListener('click', () => this.toggleDock());
    this.minimizeBtn.addEventListener('click', () => this.toggleMinimize());
    this.fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
    this.closeBtn.addEventListener('click', () => this.closeChat());
    
    // Chat buttons
    document.querySelectorAll('.chat-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const query = e.target.closest('.chat-btn').getAttribute('data-query');
        this.handleButtonClick(query);
      });
    });
    
    // Download button
    this.downloadBtn.addEventListener('click', () => this.downloadData());
    
    // Make header draggable
    this.makeDraggable();
  }
  
  toggleChat() {
    if (this.chatWindow.style.display === 'none' || !this.chatWindow.style.display) {
      this.showChat();
    } else {
      this.hideChat();
    }
  }
  
  showChat() {
    this.chatWindow.style.display = 'flex';
    this.chatToggle.style.display = 'none';
    this.isHidden = false;
    this.saveState();
  }
  
  hideChat() {
    this.chatWindow.style.display = 'none';
    this.showChatToggle();
    this.isHidden = true;
    this.saveState();
  }
  
  showChatToggle() {
    this.chatToggle.style.display = 'block';
  }
  
  toggleMinimize() {
    this.isMinimized = !this.isMinimized;
    this.chatWindow.classList.toggle('minimized', this.isMinimized);
    
    if (this.isMinimized) {
      this.chatMessages.style.display = 'none';
      document.querySelector('.chat-buttons-container').style.display = 'none';
      this.downloadSection.style.display = 'none';
    } else {
      this.chatMessages.style.display = 'block';
      document.querySelector('.chat-buttons-container').style.display = 'block';
      if (this.currentData) {
        this.downloadSection.style.display = 'block';
      }
    }
    
    this.saveState();
  }
  
  toggleFullscreen() {
    this.isFullscreen = !this.isFullscreen;
    this.chatWindow.classList.toggle('fullscreen', this.isFullscreen);
    
    if (this.isFullscreen) {
      this.chatWindow.style.width = 'auto';
      this.chatWindow.style.height = 'auto';
    } else {
      this.chatWindow.style.width = '450px';
      this.chatWindow.style.height = '600px';
    }
    
    this.saveState();
  }
  
  toggleDock() {
    this.isDocked = !this.isDocked;
    this.chatWindow.classList.toggle('docked', this.isDocked);
    this.saveState();
  }
  
  closeChat() {
    this.hideChat();
  }
  
  makeDraggable() {
    const header = this.chatWindow.querySelector('.chat-header');
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;
    
    header.addEventListener('mousedown', (e) => {
      if (this.isFullscreen || this.isDocked) return;
      
      initialX = e.clientX - xOffset;
      initialY = e.clientY - yOffset;
      
      if (e.target === header || header.contains(e.target)) {
        isDragging = true;
      }
    });
    
    document.addEventListener('mousemove', (e) => {
      if (isDragging) {
        e.preventDefault();
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
        xOffset = currentX;
        yOffset = currentY;
        
        this.chatWindow.style.transform = `translate(${currentX}px, ${currentY}px)`;
      }
    });
    
    document.addEventListener('mouseup', () => {
      isDragging = false;
    });
  }
  
  async handleButtonClick(query) {
    // Add user message
    this.addMessage(query, 'user');
    
    // Show typing indicator
    this.showTypingIndicator();
    
    try {
      // Get CSRF token
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
      
      // Send to backend
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ message: query })
      });
      
      const data = await response.json();
      
      // Remove typing indicator
      this.removeTypingIndicator();
      
      // Store current data and query for download
      this.currentData = data.data;
      this.currentQuery = query;
      
      // Add assistant response
      this.addMessage(data.response, 'assistant', data.data);
      
      // Show download section if there's data
      if (data.data && data.data.length > 0) {
        this.downloadSection.style.display = 'block';
      } else {
        this.downloadSection.style.display = 'none';
      }
      
    } catch (error) {
      console.error('Chat error:', error);
      this.removeTypingIndicator();
      this.addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    }
  }
  
  async downloadData() {
    if (!this.currentData || !this.currentQuery) return;
    
    try {
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
      
      const response = await fetch('/api/chat/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ 
          query: this.currentQuery,
          data: this.currentData 
        })
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.currentQuery.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        console.error('Download failed');
      }
    } catch (error) {
      console.error('Download error:', error);
    }
  }
  
  addMessage(content, type, data = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (type === 'user') {
      messageContent.innerHTML = `
        <i class="bi bi-person"></i>
        <div>${content}</div>
      `;
    } else if (type === 'assistant') {
      let responseContent = `<i class="bi bi-robot"></i><div><strong>Fleet Assistant:</strong> ${content}`;
      
      if (data && data.length > 0) {
        responseContent += this.formatDataTable(data);
      }
      
      responseContent += '</div>';
      messageContent.innerHTML = responseContent;
    }
    
    messageDiv.appendChild(messageContent);
    this.chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }
  
  formatDataTable(data) {
    if (!data || data.length === 0) return '';
    
    const columns = Object.keys(data[0]);
    let tableHTML = '<div style="margin-top: 10px; overflow-x: auto;"><table class="data-table">';
    
    // Header
    tableHTML += '<thead><tr>';
    columns.forEach(col => {
      tableHTML += `<th>${col.replace(/_/g, ' ').toUpperCase()}</th>`;
    });
    tableHTML += '</tr></thead>';
    
    // Body
    tableHTML += '<tbody>';
    data.forEach(row => {
      tableHTML += '<tr>';
      columns.forEach(col => {
        let value = row[col] || '';
        
        // Format status badges
        if (col.includes('status') && value) {
          const statusClass = this.getStatusClass(value);
          value = `<span class="status-badge ${statusClass}">${value}</span>`;
        }
        
        tableHTML += `<td>${value}</td>`;
      });
      tableHTML += '</tr>';
    });
    tableHTML += '</tbody></table></div>';
    
    return tableHTML;
  }
  
  getStatusClass(status) {
    const statusLower = status.toLowerCase();
    if (statusLower.includes('active') || statusLower.includes('completed') || statusLower.includes('paid')) {
      return 'status-active';
    } else if (statusLower.includes('pending')) {
      return 'status-pending';
    } else if (statusLower.includes('cancelled') || statusLower.includes('unpaid')) {
      return 'status-cancelled';
    }
    return '';
  }
  
  showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = 'typing-indicator';
    
    typingDiv.innerHTML = `
      <div class="message-content">
        <i class="bi bi-robot"></i>
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    `;
    
    this.chatMessages.appendChild(typingDiv);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }
  
  removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
      typingIndicator.remove();
    }
  }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new FleetChat();
}); 