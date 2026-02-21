import asyncio
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk

from conexao import dispositivos_salvos, varredura, testar_conexao, _ler_snapshot
from dispositivo import Dispositivo

# ---- Helpers para cores ----
def hex_to_rgb(h: str) -> tuple[int, int, int]:
	h = h.lstrip('#')
	return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r: int, g: int, b: int) -> str:
	return f"#{r:02x}{g:02x}{b:02x}"

def mix_to_white(hex_color: str, intensity: float) -> str:
	# intensity 0..1, mistura com branco para simular mais "luz"
	r, g, b = hex_to_rgb(hex_color)
	r = int(r + intensity * (255 - r))
	g = int(g + intensity * (255 - g))
	b = int(b + intensity * (255 - b))
	return rgb_to_hex(r, g, b)

def lerp_color(a: str, b: str, t: float) -> str:
	# t 0..1, interpola entre duas cores hex
	ar, ag, ab = hex_to_rgb(a)
	br, bg, bb = hex_to_rgb(b)
	r = int(ar + (br - ar) * t)
	g = int(ag + (bg - ag) * t)
	b = int(ab + (bb - ab) * t)
	return rgb_to_hex(r, g, b)

def create_neon_canvas(parent, text: str, base_color: str) -> tk.Canvas:
	# Simula um brilho neon desenhando várias camadas de texto em um Canvas
	c = tk.Canvas(parent, width=28, height=24, highlightthickness=0)
	# Camada de "glow" por trás (cores mais claras)
	for off in (1, 0, -1):
		glow = mix_to_white(base_color, 0.6)
		c.create_text(14+off, 12, text=text, fill=glow, font=('Segoe UI', 12, 'bold'))
	# Texto principal
	c.create_text(14, 12, text=text, fill=base_color, font=('Segoe UI', 12, 'bold'))
	return c


class ControlPanel(ttk.Frame):
	"""Painel único de controles que atua sobre o dispositivo selecionado."""
	def __init__(self, master: tk.Widget, get_selected_device, executor: ThreadPoolExecutor):
		super().__init__(master)
		self.get_selected_device = get_selected_device
		self.executor = executor
		self.is_on = True

		# Cabeçalho e botão de energia
		header = ttk.Frame(self)
		header.pack(fill='x', pady=(6, 8))
		ttk.Label(header, text='Controles do Dispositivo', font=('Segoe UI', 10, 'bold')).pack(side='left')
		self.power_btn = ttk.Button(header, text='⏻', width=6, command=self._power_off)
		self.power_btn.pack(side='right')

		# Brilho - label com neon e slider
		self.lbl_brightness = ttk.Label(self, text='Brightness')
		self.lbl_brightness.pack(anchor='w')
		self.brightness_scale = tk.Scale(self, from_=1, to=100, orient='horizontal', length=220)
		self.brightness_scale.pack(fill='x')
		self.brightness_scale.bind('<ButtonRelease-1>', self._apply_brightness)

		# Temperatura (White)
		self.ct_var = tk.IntVar(value=0)
		self.lbl_temp = ttk.Label(self, text='Temperature (White)')
		self.lbl_temp.pack(anchor='w', pady=(8, 0))
		self.ct_scale = tk.Scale(self, from_=0, to=100, orient='horizontal', variable=self.ct_var, length=220)
		self.ct_scale.pack(fill='x')
		self.ct_scale.bind('<ButtonRelease-1>', self._apply_temperature)

		# RGB
		ttk.Label(self, text='Color (RGB)').pack(anchor='w', pady=(8, 4))
		self.r_var = tk.IntVar(value=0)
		self.g_var = tk.IntVar(value=0)
		self.b_var = tk.IntVar(value=0)

		row_r = ttk.Frame(self)
		row_r.pack(fill='x', pady=2)
		neon_r = create_neon_canvas(row_r, 'R', '#ff3355')
		neon_r.pack(side='left', padx=(0, 8))
		self.r_scale = tk.Scale(row_r, from_=0, to=255, orient='horizontal', variable=self.r_var, length=220)
		self.r_scale.pack(side='left', fill='x', expand=True)
		self.r_scale.bind('<ButtonRelease-1>', self._apply_color)
		self.r_scale.bind('<KeyRelease>', self._apply_color)

		row_g = ttk.Frame(self)
		row_g.pack(fill='x', pady=2)
		neon_g = create_neon_canvas(row_g, 'G', '#33ff77')
		neon_g.pack(side='left', padx=(0, 8))
		self.g_scale = tk.Scale(row_g, from_=0, to=255, orient='horizontal', variable=self.g_var, length=220)
		self.g_scale.pack(side='left', fill='x', expand=True)
		self.g_scale.bind('<ButtonRelease-1>', self._apply_color)
		self.g_scale.bind('<KeyRelease>', self._apply_color)

		row_b = ttk.Frame(self)
		row_b.pack(fill='x', pady=2)
		neon_b = create_neon_canvas(row_b, 'B', '#3399ff')
		neon_b.pack(side='left', padx=(0, 8))
		self.b_scale = tk.Scale(row_b, from_=0, to=255, orient='horizontal', variable=self.b_var, length=220)
		self.b_scale.pack(side='left', fill='x', expand=True)
		self.b_scale.bind('<ButtonRelease-1>', self._apply_color)
		self.b_scale.bind('<KeyRelease>', self._apply_color)

	def _power_off(self):
		dispositivo = self.get_selected_device()
		if not dispositivo:
			return

		def work():
			try:
				dispositivo.desligar()
				return True
			except Exception:
				return False

		self.executor.submit(work)

	def _apply_brightness(self, event=None):
		dispositivo = self.get_selected_device()
		if not dispositivo:
			return
		value = int(self.brightness_scale.get())
		# Atualiza a cor do label conforme intensidade
		base = '#00eaff'
		self.lbl_brightness.configure(foreground=mix_to_white(base, value/100.0))
		self.executor.submit(lambda: dispositivo.definir_brilho(value))

	def _apply_temperature(self, event=None):
		dispositivo = self.get_selected_device()
		if not dispositivo:
			return
		value = int(self.ct_var.get())
		# 0 quente (laranja), 100 frio (azul)
		warm = '#ff6a00'
		cold = '#00bfff'
		self.lbl_temp.configure(foreground=lerp_color(warm, cold, value/100.0))
		self.executor.submit(lambda: dispositivo.definir_temperatura(value))

	def _apply_color(self, event=None):
		dispositivo = self.get_selected_device()
		if not dispositivo:
			return
		r, g, b = self.r_var.get(), self.g_var.get(), self.b_var.get()
		self.executor.submit(lambda: dispositivo.definir_cor(r, g, b))


class InterfaceApp:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title('Hub IoT')
		self.root.geometry('420x520')

		# Executor para operações com dispositivos
		self.executor = ThreadPoolExecutor(max_workers=8)

		# Barra superior com título e ações
		top = ttk.Frame(self.root)
		top.pack(fill='x', padx=12, pady=(10, 6))
		ttk.Label(top, text='Hub IoT - Bulb Control', font=('Segoe UI', 12, 'bold')).pack(side='left')
		self.refresh_btn = ttk.Button(top, text='Atualizar', width=10, command=self._on_refresh)
		self.refresh_btn.pack(side='right', padx=(6, 0))

		# Loading/progress
		self.loading_frame = ttk.Frame(self.root)
		self.loading_frame.pack(fill='x', padx=12, pady=(0, 8))
		ttk.Label(self.loading_frame, text='Testando conexão com dispositivos...').pack(side='left')
		self.progress = ttk.Progressbar(self.loading_frame, mode='indeterminate', length=160)
		self.progress.pack(side='left', padx=(8, 0))

		# Seletor de dispositivos
		sel = ttk.Frame(self.root)
		sel.pack(fill='x', padx=12, pady=(4, 8))
		ttk.Label(sel, text='Dispositivo').pack(anchor='w', pady=(0, 4))
		self.device_combo = ttk.Combobox(sel, values=[], state='readonly')
		self.device_combo.pack(fill='x')
		self.device_combo.bind('<<ComboboxSelected>>', self._on_select_device)

		# Painel único de controles
		self.panel = ControlPanel(self.root, self._get_selected_device, self.executor)
		self.panel.pack(fill='x', padx=12, pady=(6, 12))

		# Estado interno
		self.devices: list[Dispositivo] = []
		self.device_labels: list[str] = []
		self.selected_index: int = -1
		self.device_name_by_id: dict[str, str] = {}

		# Inicializa com loading e começa carregamento
		self._start_loading()
		self._load_devices_async()

	def _refresh_name_mapping(self):
		try:
			snap = _ler_snapshot() or []
			mapping: dict[str, str] = {}
			for d in snap:
				did = d.get('id')
				name = d.get('name')
				if did and name:
					mapping[str(did)] = str(name)
			self.device_name_by_id = mapping
		except Exception:
			self.device_name_by_id = {}

	def _start_loading(self):
		self.loading_frame.pack(fill='x', padx=12, pady=(0, 8))
		try:
			self.progress.start(10)
		except Exception:
			pass

	def _stop_loading(self):
		try:
			self.progress.stop()
		except Exception:
			pass
		self.loading_frame.pack_forget()

	def _clear_devices(self):
		self.devices.clear()
		self.device_labels.clear()
		self.device_combo['values'] = []
		self.selected_index = -1
		# Desabilita controles até haver seleção
		self._set_controls_enabled(False)

	def _add_device(self, dispositivo: Dispositivo):
		bulb = dispositivo.get_bulb()
		bid = getattr(bulb, 'id', None) or '?'
		ip = getattr(bulb, 'address', None) or getattr(bulb, 'ip', None)
		name = self.device_name_by_id.get(str(bid))
		label = name if name else (f"{bid} ({ip})" if ip else str(bid))
		self.devices.append(dispositivo)
		self.device_labels.append(label)
		self.device_combo['values'] = self.device_labels
		# Seleciona primeiro dispositivo automaticamente
		if self.selected_index == -1:
			self.selected_index = 0
			self.device_combo.current(0)
			self._on_select_device()

	def _load_devices_async(self):
		# Carrega dispositivos salvos e testa cada um em paralelo
		def work():
			try:
				return dispositivos_salvos()
			except Exception:
				return []

		def on_devices_ready(fut):
			devices = fut.result() or []
			if not devices:
				self._stop_loading()
				return

			pending = len(devices)

			def on_test_done(f):
				nonlocal pending
				ok = False
				try:
					ok = f.result()
				except Exception:
					ok = False
				if ok:
					dispositivo = f.device  # anexado abaixo
					self.root.after(0, self._add_device, dispositivo)
				pending -= 1
				if pending <= 0:
					self.root.after(0, self._stop_loading)

			for d in devices:
				# Executa teste de conexão em thread chamando as funções async via asyncio.run
				def test_callable(dispositivo: Dispositivo):
					try:
						return testar_conexao(dispositivo)
					except Exception:
						return False

				fut_test = self.executor.submit(test_callable, d)
				# Monkey-patch para recuperar dispositivo ao concluir
				fut_test.device = d  # type: ignore[attr-defined]
				fut_test.add_done_callback(on_test_done)

		self._refresh_name_mapping()
		self._clear_devices()
		self._start_loading()
		self.executor.submit(work).add_done_callback(lambda f: self.root.after(0, on_devices_ready, f))

	def _on_refresh(self):
		# Dispara varredura e atualiza lista assincronamente
		self._start_loading()

		def run_scan():
			try:
				return varredura()
			except Exception:
				return False

		def after_scan(_: object):
			# Recarrega dispositivos independentemente do sucesso, pois snapshot pode ter mudado
			self._load_devices_async()

		self.executor.submit(run_scan).add_done_callback(lambda f: self.root.after(0, after_scan, f))

	def _get_selected_device(self) -> Dispositivo | None:
		if 0 <= self.selected_index < len(self.devices):
			return self.devices[self.selected_index]
		return None

	def _set_controls_enabled(self, enabled: bool):
		state = 'normal' if enabled else 'disabled'
		for w in [
			self.panel.brightness_scale,
			self.panel.ct_scale,
			self.panel.r_scale,
			self.panel.g_scale,
			self.panel.b_scale,
			self.panel.power_btn,
		]:
			try:
				w.configure(state=state)
			except Exception:
				pass

	def _on_select_device(self, event=None):
		self.selected_index = self.device_combo.current()
		dispositivo = self._get_selected_device()
		if not dispositivo:
			self._set_controls_enabled(False)
			return

		self._set_controls_enabled(True)

		# Lê estado atual do dispositivo em thread e atualiza os controles
		def read_state():
			try:
				b = dispositivo.get_bulb()
				vals = {}
				try:
					vals['brightness'] = int(getattr(b, 'get_brightness_percentage')())
				except Exception:
					vals['brightness'] = None
				try:
					vals['ct'] = int(getattr(b, 'get_colourtemp_percentage')())
				except Exception:
					vals['ct'] = None
				try:
					r, g, bb = b.colour_rgb()
					vals['r'], vals['g'], vals['b'] = r, g, bb
				except Exception:
					vals['r'] = vals['g'] = vals['b'] = None
				return vals
			except Exception:
				return {'brightness': None, 'ct': None, 'r': None, 'g': None, 'b': None}

		def apply_vals(fut):
			vals = fut.result() or {}
			if vals.get('brightness') is not None:
				self.panel.brightness_scale.set(vals['brightness'])
			if vals.get('ct') is not None:
				self.panel.ct_var.set(vals['ct'])
				self.panel.ct_scale.set(vals['ct'])
			if vals.get('r') is not None:
				self.panel.r_var.set(vals['r'])
				self.panel.g_var.set(vals['g'])
				self.panel.b_var.set(vals['b'])
				self.panel.r_scale.set(vals['r'])
				self.panel.g_scale.set(vals['g'])
				self.panel.b_scale.set(vals['b'])

		self.executor.submit(read_state).add_done_callback(lambda f: self.root.after(0, apply_vals, f))

	def run(self):
		self.root.mainloop()


if __name__ == '__main__':
	# A interface é a primeira coisa a ser carregada
	app = InterfaceApp()
	app.run()

