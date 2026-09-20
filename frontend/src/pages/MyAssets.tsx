import { useEffect, useState } from 'react';
import { api } from '../api/client';

type Asset={id:string;name:string;description:string;price:number;purchased_at:string|null};
export default function MyAssets(){const [assets,setAssets]=useState<Asset[]>([]);const [error,setError]=useState('');useEffect(()=>{api<{assets:Asset[]}>('/api/dashboard/my-assets').then(r=>setAssets(r.assets)).catch(e=>setError((e as Error).message))},[]);return <><div className="hero"><div><p className="eyebrow">USER AREA</p><h1>My assets</h1><p>Only assets owned by your account are shown here.</p></div></div>{error&&<p className="error">{error}</p>}<div className="grid">{assets.length?assets.map(a=><article className="card" key={a.id}><h3>{a.name}</h3><p>{a.description}</p><strong>${a.price.toFixed(2)}</strong><p className="muted">Purchased {a.purchased_at?new Date(a.purchased_at).toLocaleString():'-'}</p></article>):<div className="card"><p>You haven't purchased any assets yet.</p></div>}</div></>}
