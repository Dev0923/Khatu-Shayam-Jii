import { useEffect, useRef, useState, useCallback } from "react";
import { AlertTriangle, Info, XCircle, X, Bell } from "lucide-react";

/* ─── Types ──────────────────────────────────────────────── */
interface AlertMsg {
  id: number;
  message: string;
  severity: "info" | "warning" | "critical";
  timestamp: string;
}

/* ─── Severity styling ───────────────────────────────────── */
const SEV = {
  info: {
    bg: "linear-gradient(135deg, #1F2F8C 0%, #2a3fa8 100%)",
    border: "#3B5BDB",
    icon: <Info size={22} color="#fff" />,
    glow: "0 0 30px rgba(59,91,219,0.35)",
    label: "Information",
  },
  warning: {
    bg: "linear-gradient(135deg, #D97706 0%, #F59E0B 100%)",
    border: "#F59E0B",
    icon: <AlertTriangle size={22} color="#fff" />,
    glow: "0 0 30px rgba(245,158,11,0.35)",
    label: "Warning",
  },
  critical: {
    bg: "linear-gradient(135deg, #DC2626 0%, #EF4444 100%)",
    border: "#EF4444",
    icon: <XCircle size={22} color="#fff" />,
    glow: "0 0 30px rgba(239,68,68,0.35)",
    label: "Critical Alert",
  },
};

/* ─── Durations (auto-dismiss) ───────────────────────────── */
const DURATION: Record<string, number> = {
  info: 8000,
  warning: 12000,
  critical: 20000,
};

let _idCounter = 0;

/* ═══════════════════════════════════════════════════════════
   AlertListener — mounts once in App.tsx, shows toasts
═══════════════════════════════════════════════════════════ */
export function AlertListener() {
  const [alerts, setAlerts] = useState<AlertMsg[]>([]);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>();

  const dismiss = useCallback((id: number) => {
    setAlerts((prev) => prev.filter((a) => a.id !== id));
  }, []);

  /* ── Connect / reconnect logic ─────────────────────────── */
  const connect = useCallback(() => {
    // Determine WS URL from current page location
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const host = window.location.hostname;
    const wsUrl = `${proto}://${host}:8000/api/v1/alerts/ws`;

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("[AlertListener] WebSocket connected");
    };

    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === "alert") {
          const id = ++_idCounter;
          const newAlert: AlertMsg = {
            id,
            message: data.message,
            severity: data.severity || "info",
            timestamp: data.timestamp,
          };
          setAlerts((prev) => [...prev, newAlert]);

          // Auto-dismiss
          const dur = DURATION[newAlert.severity] ?? 8000;
          setTimeout(() => dismiss(id), dur);
        }
      } catch {
        /* ignore non-JSON frames */
      }
    };

    ws.onclose = () => {
      console.log("[AlertListener] WebSocket closed — reconnecting in 3s");
      reconnectTimer.current = setTimeout(connect, 3000);
    };

    ws.onerror = () => {
      ws.close();
    };
  }, [dismiss]);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, [connect]);

  /* ── Nothing to render ─────────────────────────────────── */
  if (alerts.length === 0) return null;

  /* ── Toast stack (bottom-right) ────────────────────────── */
  return (
    <div
      id="alert-toast-stack"
      style={{
        position: "fixed",
        bottom: 24,
        right: 24,
        zIndex: 99999,
        display: "flex",
        flexDirection: "column-reverse",
        gap: 12,
        maxWidth: 420,
        width: "100%",
        pointerEvents: "none",
      }}
    >
      {alerts.map((a) => {
        const s = SEV[a.severity] ?? SEV.info;
        return (
          <div
            key={a.id}
            style={{
              pointerEvents: "auto",
              background: s.bg,
              border: `1.5px solid ${s.border}`,
              borderRadius: 16,
              padding: "16px 18px",
              boxShadow: `${s.glow}, 0 8px 32px rgba(0,0,0,0.25)`,
              color: "#fff",
              fontFamily: "system-ui, -apple-system, sans-serif",
              animation: "alertSlideIn 0.4s cubic-bezier(0.16,1,0.3,1)",
            }}
          >
            {/* Header row */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                marginBottom: 8,
              }}
            >
              <div
                style={{
                  width: 36,
                  height: 36,
                  borderRadius: 10,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: "rgba(255,255,255,0.15)",
                  flexShrink: 0,
                }}
              >
                {s.icon}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                    marginBottom: 2,
                  }}
                >
                  <Bell size={11} color="rgba(255,255,255,0.7)" />
                  <span
                    style={{
                      fontSize: 10,
                      fontWeight: 800,
                      textTransform: "uppercase",
                      letterSpacing: "0.08em",
                      color: "rgba(255,255,255,0.75)",
                    }}
                  >
                    {s.label}
                  </span>
                </div>
                <span
                  style={{
                    fontSize: 9,
                    color: "rgba(255,255,255,0.5)",
                  }}
                >
                  Khatu Shyam Ji Temple
                </span>
              </div>
              <button
                onClick={() => dismiss(a.id)}
                style={{
                  background: "rgba(255,255,255,0.12)",
                  border: "none",
                  borderRadius: 8,
                  padding: 6,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                }}
              >
                <X size={14} color="#fff" />
              </button>
            </div>

            {/* Message */}
            <p
              style={{
                fontSize: 14,
                fontWeight: 600,
                lineHeight: 1.5,
                margin: 0,
                paddingLeft: 46,
              }}
            >
              {a.message}
            </p>
          </div>
        );
      })}

      {/* Keyframe animation (injected once) */}
      <style>{`
        @keyframes alertSlideIn {
          from { opacity: 0; transform: translateX(80px) scale(0.92); }
          to   { opacity: 1; transform: translateX(0) scale(1); }
        }
      `}</style>
    </div>
  );
}
