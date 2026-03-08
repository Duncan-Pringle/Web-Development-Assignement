//Admin Dashboard User Interface
export function renderAdmin(){
    return `
     <div class="view">
     <h2>Admin Dashboard</h2>
     <div class="admin-panel">
     <div class ="panel">
     <h3>Moderate Reviews</h3>
     <div id="reviewAdminList"></div>
     </div>
     
     <div class="panel">
     <h3>User Management</h3>
     <div id="userList"></div>
     </div>
     </div>
     </div>
     
    `;
}