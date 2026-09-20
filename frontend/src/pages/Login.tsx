import { FormEvent, useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Login({ onDone }: { onDone: () => void }) {
  const { login } = useAuth(); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [error,setError]=useState('');
  const submit=async(e:FormEvent)=>{e.preventDefault();setError('');try{await login(email,password);onDone();}catch(err){setError((err as Error).message)}};
  return <section className="card form"><h2>Login</h2><form onSubmit={submit}><input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/><input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} required/><button className="primary">Login</button>{error&&<p className="error">{error}</p>}</form></section>;
}
