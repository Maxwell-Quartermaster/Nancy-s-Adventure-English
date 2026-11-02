f = os.path.join(os.environ['GATE_SB'], 'snap-r2h-0021MDT', 'QUEUE.md'); os.chmod(os.path.dirname(f), 0o755); os.chmod(f, 0o644); open(f, 'a').write('tampered after the carry check (Auditor gate)\n')
