<h1 id="inscribe.ai">Inscribe.ai</h1>
<ul>
<li>API wrapper for <a href="https://inscribe.ai">Inscribe</a></li>
</ul>
<p>For more information, please read our <a href="https://docs.inscribe.ai/#introduction">documentation</a>.</p>
<h2 id="installation">Installation</h2>
<ul>
<li><code>pip install inscribe</code></li>
</ul>
<h2 id="usage">Usage</h2>
<div class="sourceCode" id="cb1"><pre class="sourceCode python"><code class="sourceCode python"><a class="sourceLine" id="cb1-1" title="1"><span class="im">import</span> inscribe</a>
<a class="sourceLine" id="cb1-2" title="2"><span class="im">import</span> json</a>
<a class="sourceLine" id="cb1-3" title="3"></a>
<a class="sourceLine" id="cb1-4" title="4"><span class="co"># API Authentication</span></a>
<a class="sourceLine" id="cb1-5" title="5">api <span class="op">=</span> inscribe.Client(api_key<span class="op">=</span><span class="st">&quot;YOUR_API_KEY&quot;</span>)</a>
<a class="sourceLine" id="cb1-6" title="6"></a>
<a class="sourceLine" id="cb1-7" title="7"><span class="co"># Create customer folder</span></a>
<a class="sourceLine" id="cb1-8" title="8">customer <span class="op">=</span> api.create_customer(customer_name<span class="op">=</span><span class="st">&quot;new&quot;</span>)</a>
<a class="sourceLine" id="cb1-9" title="9">customer_id <span class="op">=</span> customer[<span class="st">&#39;data&#39;</span>][<span class="st">&#39;id&#39;</span>]</a>
<a class="sourceLine" id="cb1-10" title="10"></a>
<a class="sourceLine" id="cb1-11" title="11"><span class="co"># Upload document</span></a>
<a class="sourceLine" id="cb1-12" title="12">doc_obj <span class="op">=</span> <span class="bu">open</span>(<span class="st">&quot;YOUR_FILE.pdf&quot;</span>, <span class="st">&quot;rb&quot;</span>)</a>
<a class="sourceLine" id="cb1-13" title="13">document <span class="op">=</span> api.upload_document(customer_id<span class="op">=</span>customer_id, document<span class="op">=</span>doc_obj)</a>
<a class="sourceLine" id="cb1-14" title="14">document_id <span class="op">=</span> document[<span class="st">&#39;result_urls&#39;</span>][<span class="dv">0</span>][<span class="st">&#39;document_id&#39;</span>]</a>
<a class="sourceLine" id="cb1-15" title="15"></a>
<a class="sourceLine" id="cb1-16" title="16"><span class="co"># Check document</span></a>
<a class="sourceLine" id="cb1-17" title="17">result <span class="op">=</span> api.check_document(customer_id<span class="op">=</span>customer_id, document_id<span class="op">=</span>document_id)</a>
<a class="sourceLine" id="cb1-18" title="18"><span class="bu">print</span>(json.dumps(result, indent<span class="op">=</span><span class="dv">2</span>))</a></code></pre></div>

pandoc 2.7.2