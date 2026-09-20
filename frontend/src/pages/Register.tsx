import { FormEvent, useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function Register({ onDone }: { onDone: () => void }) {
  const { register } = useAuth(); const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [password,setPassword]=useState(''); const [error,setError]=useState('');
  const submit=async(e:FormEvent)=>{e.preventDefault();setError('');try{await register(name,email,password);onDone();}catch(err){setError((err as Error).message)}};
  return <section className="card form"><h2>Create account</h2><form onSubmit={submit}><input placeholder="Full name" value={name} onChange={e=>setName(e.target.value)} required minLength={2}/><input type="email" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required/><input type="password" placeholder="Password (8+ chars)" value={password} onChange={e=>setPassword(e.target.value)} required minLength={8}/><button className="primary">Register</button>{error&&<p className="error">{error}</p>}</form></section>;
}
