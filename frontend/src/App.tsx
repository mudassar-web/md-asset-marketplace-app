import { useState } from 'react';
import Nav from './components/Nav';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import MyAssets from './pages/MyAssets';
import Admin from './pages/Admin';
import { useAuth } from './context/AuthContext';
import './styles.css';

export default function App(){
  const {user,loading}=useAuth(); const [page,setPage]=useState('dashboard');
  if(loading) return <div className="loading">Loading session...</div>;
  const navigate=(next:string)=>setPage(next);
  let content=<Dashboard/>;
  if(page==='login'&&!user) content=<Login onDone={()=>navigate('dashboard')}/>;
  else if(page==='register'&&!user) content=<Register onDone={()=>navigate('dashboard')}/>;
  else if(page==='my-assets'&&user) content=<MyAssets/>;
  else if(page==='admin'&&user?.role==='admin') content=<Admin/>;
  return <><Nav page={page} setPage={navigate}/><main>{content}</main></>;
}
