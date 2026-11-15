import { NavLink } from "react-router-dom";
import { LayoutDashboard, PlusCircle, History, HeartPulse, Siren } from "lucide-react";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/incidents/new", label: "New Incident", icon: PlusCircle },
  { to: "/history", label: "History", icon: History },
  { to: "/health", label: "Backend Health", icon: HeartPulse },
];

export default function Layout({ children }) {
  return (
    <div className="min-h-screen md:flex">
      <aside className="border-b border-slate-800 bg-slate-900 md:min-h-screen md:w-60 md:border-b-0 md:border-r">
        <div className="flex items-center gap-2 px-5 py-4 text-slate-100">
          <Siren className="h-6 w-6 text-indigo-400" />
          <span className="font-semibold">IT Incident War-Room</span>
        </div>
        <nav className="flex gap-1 overflow-x-auto px-3 pb-3 md:flex-col md:pb-0">
          {links.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-2 whitespace-nowrap rounded-lg px-3 py-2 text-sm transition ${
                  isActive ? "bg-indigo-600/20 text-indigo-300" : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                }`
              }
            >
              <Icon className="h-4 w-4" /> {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="mx-auto w-full max-w-6xl flex-1 p-4 md:p-8">{children}</main>
    </div>
  );
}
