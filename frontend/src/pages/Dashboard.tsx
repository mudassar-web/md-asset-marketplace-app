import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';

type Asset={id:string;name:string;description:string;price:number;owner_id:string|null;created_at:string;purchased_at:string|null};

function AssetCard({asset,onBuy}:{asset:Asset;onBuy:()=>void}){const {user}=useAuth();return <article className="card"><h3>{asset.name}</h3><p>{asset.description}</p><strong>${asset.price.toFixed(2)}</strong>{user?<button className="primary" onClick={onBuy}>Buy asset</button>:<p className="muted">Login to purchase</p>}</article>}

export default function Dashboard(){const {user}=useAuth();const [assets,setAssets]=useState<Asset[]>([]);const [error,setError]=useState('');const load=async()=>{try{const r=await api<{assets:Asset[]}>('/api/dashboard/assets');setAssets(r.assets)}catch(e){setError((e as Error).message)}};useEffect(()=>{void load()},[]);const buy=async(id:string)=>{try{await api(`/api/dashboard/assets/${id}/buy`,{method:'POST'});await load()}catch(e){setError((e as Error).message)}};return <><div className="hero"><div><p className="eyebrow">DASHBOARD</p><h1>Available assets</h1><p>Browse assets publicly. Sign in when you're ready to purchase.</p></div>{user&&<span className="badge">Signed in as {user.name}</span>}</div>{error&&<p className="error">{error}</p>}<div className="grid">{assets.length?assets.map(a=><AssetCard key={a.id} asset={a} onBuy={()=>void buy(a.id)}/>):<div className="card"><p>No assets are currently available.</p></div>}</div></>}
