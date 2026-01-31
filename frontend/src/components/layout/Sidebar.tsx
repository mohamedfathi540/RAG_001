import { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  ChatBubbleLeftRightIcon,
  ArrowUpTrayIcon,
  MagnifyingGlassIcon,
  ChartBarIcon,
  Cog6ToothIcon,
} from "@heroicons/react/24/outline";
import { useSettingsStore } from "../../stores/settingsStore";
import { StatusBadge } from "../ui/StatusBadge";
import { Button } from "../ui/Button";
import { checkHealth } from "../../api/base";

const navigation = [
  { name: "Chat", href: "/", icon: ChatBubbleLeftRightIcon },
  { name: "Upload & Process", href: "/upload", icon: ArrowUpTrayIcon },
  { name: "Search", href: "/search", icon: MagnifyingGlassIcon },
  { name: "Index Info", href: "/index", icon: ChartBarIcon },
  { name: "Settings", href: "/settings", icon: Cog6ToothIcon },
];

export function Sidebar() {
  const { projectId, setProjectId, apiUrl } = useSettingsStore();
  const [apiStatus, setApiStatus] = useState<"online" | "offline">("offline");
  const [isChecking, setIsChecking] = useState(false);

  const checkApiStatus = async () => {
    setIsChecking(true);
    try {
      await checkHealth();
      setApiStatus("online");
    } catch {
      setApiStatus("offline");
    } finally {
      setIsChecking(false);
    }
  };

  return (
    <aside className="w-64 bg-bg-secondary border-r border-border flex flex-col h-full">
      {/* Logo */}
      <div className="p-6 border-b border-border">
        <h1 className="text-2xl font-bold gradient-primary bg-clip-text text-transparent">
          Fehres
        </h1>
        <p className="text-xs text-text-secondary mt-1">RAG System</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive ?
                  "bg-primary-500/10 text-primary-400 border border-primary-500/20"
                : "text-text-secondary hover:bg-bg-hover hover:text-text-primary"
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Project & Status */}
      <div className="p-4 border-t border-border space-y-4">
        {/* Project ID */}
        <div>
          <label className="text-xs font-medium text-text-secondary uppercase tracking-wider">
            Project ID
          </label>
          <input
            type="number"
            min={1}
            value={projectId}
            onChange={(e) => setProjectId(parseInt(e.target.value) || 1)}
            className="mt-1 w-full px-3 py-2 bg-bg-primary border border-border rounded-lg text-sm text-text-primary focus:outline-none focus:border-primary-500"
          />
        </div>

        {/* API Status */}
        <div className="flex items-center justify-between">
          <StatusBadge
            status={apiStatus}
            text={isChecking ? "Checking..." : undefined}
          />
          <Button
            variant="ghost"
            size="sm"
            onPress={checkApiStatus}
            isLoading={isChecking}
          >
            Check
          </Button>
        </div>

        {/* API URL */}
        <p className="text-xs text-text-muted truncate" title={apiUrl}>
          {apiUrl}
        </p>
      </div>
    </aside>
  );
}
