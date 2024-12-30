<script>
	import '../app.css';
	export const prerender = true;
	let { children } = $props();
</script>

{@render children()}
