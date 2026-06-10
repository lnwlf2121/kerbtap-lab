use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::net::UdpSocket;
use tokio::sync::Mutex;

pub struct PrizmaticKnockSieve {
    target_sequence: Vec<u128>,
    incoming_timestamps: Vec<Instant>,
    allowed_window_ms: u128,
    is_gate_unlocked: bool,
}

impl PrizmaticKnockSieve {
    pub fn new(custom_intervals: Vec<u128>) -> Self {
        Self {
            target_sequence: custom_intervals,
            incoming_timestamps: Vec::new(),
            allowed_window_ms: 250,
            is_gate_unlocked: false,
        }
    }

    pub fn register_raw_knock(&mut self) -> bool {
        let now = Instant::now();
        self.incoming_timestamps.push(now);

        if self.incoming_timestamps.len() > self.target_sequence.len() + 1 {
            self.incoming_timestamps.remove(0);
        }

        if self.incoming_timestamps.len() == self.target_sequence.len() + 1 {
            let mut matched_pattern = true;

            for i in 0..self.target_sequence.len() {
                let actual_delta = self.incoming_timestamps[i + 1]
                    .duration_since(self.incoming_timestamps[i])
                    .as_millis();
                
                let target_delta = self.target_sequence[i];
                let upper_bound = target_delta + self.allowed_window_ms;
                let lower_bound = target_delta.saturating_sub(self.allowed_window_ms);

                if actual_delta < lower_bound || actual_delta > upper_bound {
                    matched_pattern = false;
                    break;
                }
            }

            if matched_pattern {
                println!("[Prizmatic Protocol] Shave-and-a-Haircut sequence verified! Gateway unlocked.");
                self.is_gate_unlocked = true;
                self.incoming_timestamps.clear();
                return true;
            }
        }
        false
    }

    pub fn gateway_status(&self) -> bool {
        self.is_gate_unlocked
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::Builder::new().filter(None, log::LevelFilter::Info).init();

    println!("==========================================================================");
    println!("        CHROMALON CODES: PRIZMATIC LAB ENGINE v2.1.0 ACTIVATED             ");
    println!("==========================================================================");

    // "Shave and a Haircut... 2 bits" temporal intervals (ms)
    let user_defined_intervals = vec![500, 250, 250, 500, 750, 250];
    let knock_engine = Arc::new(Mutex::new(PrizmaticKnockSieve::new(user_defined_intervals)));

    let socket = Arc::new(UdpSocket::bind("0.0.0.0:9999").await?);
    let mut buf = vec![0u8; 2048];

    loop {
        let (size, src_addr) = socket.recv_from(&mut buf).await?;
        let mut engine = knock_engine.lock().await;

        if size == 1 { 
            if engine.register_raw_knock() {
                println!("[Handshake Matrix] Core interface bypassed firewall blocking for peer: {}", src_addr);
                continue;
            }
        }

        if engine.gateway_status() {
            // Process raw fluid telemetry frames natively out-of-band
        }
    }
}
