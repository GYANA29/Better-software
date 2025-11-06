let currentTask = null;

const el = (id) => document.getElementById(id);

async function createTask(title) {
	const res = await fetch('/tasks/', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ title }),
	});
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

async function listComments(taskId) {
	const res = await fetch(`/tasks/${taskId}/comments`);
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

async function createComment(taskId, payload) {
	const res = await fetch(`/tasks/${taskId}/comments`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload),
	});
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

async function updateComment(commentId, patch) {
	const res = await fetch(`/comments/${commentId}`, {
		method: 'PATCH',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(patch),
	});
	if (!res.ok) throw new Error(await res.text());
	return res.json();
}

async function deleteComment(commentId) {
	const res = await fetch(`/comments/${commentId}`, { method: 'DELETE' });
	if (!res.ok) throw new Error(await res.text());
	return true;
}

async function refreshComments() {
	if (!currentTask) return;
	const list = await listComments(currentTask.id);
	const ul = el('comments');
	ul.innerHTML = '';
	for (const c of list) {
		const li = document.createElement('li');
		const span = document.createElement('span');
		span.style.flex = '1';
		span.innerText = `${c.author}: ${c.content}`;
		const edit = document.createElement('button');
		edit.innerText = 'Edit';
		edit.onclick = async () => {
			try {
				let content = prompt('Edit content:', c.content);
				if (content === null) return; // cancelled
				content = content.trim();
				if (!content) { alert('Content cannot be empty'); return; }
				await updateComment(c.id, { content });
				await refreshComments();
			} catch (e) {
				alert(e.message || String(e));
			}
		};
		const del = document.createElement('button');
		del.innerText = 'Delete';
		del.onclick = async () => {
			try {
				if (!confirm('Delete this comment?')) return;
				await deleteComment(c.id);
				await refreshComments();
			} catch (e) {
				alert(e.message || String(e));
			}
		};
		li.appendChild(span);
		li.appendChild(edit);
		li.appendChild(del);
		ul.appendChild(li);
	}
}

el('createTaskBtn').onclick = async () => {
	const title = el('taskTitle').value.trim();
	if (!title) return alert('Enter task title');
	try {
		currentTask = await createTask(title);
		const info = el('taskInfo');
		info.style.display = 'block';
		info.innerText = `Task ID: ${currentTask.id} | Title: ${currentTask.title}`;
		await refreshComments();
	} catch (e) {
		alert(e.message || String(e));
	}
};

el('addCommentBtn').onclick = async () => {
	if (!currentTask) return alert('Create a task first');
	const author = el('author').value.trim();
	const content = el('content').value.trim();
	if (!author || !content) return alert('Enter author and content');
	try {
		await createComment(currentTask.id, { author, content });
		el('author').value = '';
		el('content').value = '';
		await refreshComments();
	} catch (e) {
		alert(e.message || String(e));
	}
};


