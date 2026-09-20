import { useAuth } from '../context/AuthContext';

export default function Nav({ page, setPage }: { page: string; setPage: (page: string) => void }) {
  const { user, logout } = useAuth();
  return <header className="nav">
    <div className='logo-container'><img src='/src/assets/MD.png' height='60 px' width='60 px' /><span className='title'>Asset Marketplace App</span><span className="tagline">A complete trading experience</span></div>
    <nav>
      <button className={page === 'dashboard' ? 'active' : ''} onClick={() => setPage('dashboard')}>Dashboard</button>
      {user && <button className={page === 'my-assets' ? 'active' : ''} onClick={() => setPage('my-assets')}>My Assets</button>}
      {user?.role === 'admin' && <button className={page === 'admin' ? 'active' : ''} onClick={() => setPage('admin')}>Admin</button>}
      {!user ? <><button onClick={() => setPage('login')}>Login</button><button onClick={() => setPage('register')}>Register</button></> : <button onClick={() => void logout()}>Logout</button>}
    </nav>
  </header>;
}
