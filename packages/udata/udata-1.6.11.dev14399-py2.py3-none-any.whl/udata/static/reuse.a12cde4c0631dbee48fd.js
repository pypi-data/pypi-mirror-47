webpackJsonp([38],{0:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}s(977);var i=s(74),o=_interopRequireDefault(i),a=s(5),n=_interopRequireDefault(a),r=s(28),d=_interopRequireDefault(r),u=s(340),c=_interopRequireDefault(u),l=s(500),p=_interopRequireDefault(l),f=s(281),m=_interopRequireDefault(f),b=s(501),h=_interopRequireDefault(b),v=s(502),g=_interopRequireDefault(v),A=s(335),_=_interopRequireDefault(A);new d.default({mixins:[o.default],components:{FollowButton:m.default,ShareButton:_.default,DiscussionThreads:c.default,FeaturedButton:p.default,IssuesButton:g.default,IntegrateButton:h.default},ready:function(){n.default.debug("Reuse display page")},methods:{suggestTag:function(){this.$refs.discussions.start(this._("New tag suggestion to improve metadata"),this._("Hello,\n\nI propose this new tag: "))}}})},69:function(e,t,s){var i,o;i=s(303),o=s(327),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},158:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(83),o=_interopRequireDefault(i);t.default={props:{classes:{type:Array,coerce:function(e){return Array.isArray(e)?e:e.split(" ").filter(function(e){return e.trim()})}},followers:{type:Number,default:void 0},following:{type:Boolean,default:!1},withLabel:{type:Boolean,default:!1},tooltip:{type:String,default:o.default._("I'll be informed about its activity")},tooltipPlacement:{type:String,default:"left"},url:{type:String,required:!0}},computed:{btnClasses:function(){var e={active:this.following};return this.classes.forEach(function(t){e[t]=!0}),e},icon:function(){return this.following?"fa-eye-slash":"fa-eye"},label:function(){return this.following?this._("Unfollow"):this._("Follow")}},methods:{toggle:function(){var e=this;this.$auth(this._("You need to be logged in to follow."));var t=this.following?this.$api.delete(this.url):this.$api.post(this.url);t.then(function(t){e.following=!e.following,void 0!==e.followers&&(e.followers=t.followers)})}}}},276:function(e,t){e.exports=' <button type=button class="btn btn-follow" :class=btnClasses @click=toggle v-tooltip=tooltip :tooltip-placement=tooltipPlacement> <span class=fa :class=icon></span> <span v-if=withLabel>{{ label }}</span> <span v-if=followers>{{ followers }}</span> </button> '},281:function(e,t,s){var i,o;i=s(158),o=s(276),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},303:function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=52;t.default={props:{user:Object,size:{type:Number,default:s}}}},304:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(83),o=(_interopRequireDefault(i),s(75)),a=_interopRequireDefault(o);t.default={props:{title:{type:String,required:!0},url:{type:String,required:!0}},filters:{encode:encodeURIComponent},methods:{click:function(){a.default.publish("SHARE"),this.$refs.popover.show=!1}}}},305:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(10),o=_interopRequireDefault(i),a=s(69),n=_interopRequireDefault(a);t.default={components:{Avatar:n.default},props:{message:Object,discussion:String,index:Number},methods:{formatDate:function(e){return(0,o.default)(e).format("LL")}}}},306:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(5),o=_interopRequireDefault(i);t.default={props:{subjectId:String,subjectClass:String,position:Number},data:function(){return{sending:!1,title:"",comment:""}},methods:{prefill:function(e,t){t=t||"",this.comment=t,this.title=e||"",e?(this.$els.textarea.setSelectionRange(t.length,t.length),this.$els.textarea.focus()):this.$els.title.focus()},submit:function(){var e=this,t={title:this.title,comment:this.comment,subject:{id:this.subjectId,class:this.subjectClass}};this.sending=!0,this.$api.post("discussions/",t).then(function(t){e.$dispatch("discussion:created",t),e.title="",e.comment="",e.sending=!1,document.location.href="#discussion-"+t.id}).catch(function(t){var s=e._("An error occured while submitting your comment");e.$dispatch("notify:error",s),o.default.error(t),e.sending=!1})}}}},307:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(5),o=_interopRequireDefault(i);t.default={props:{discussionId:String},data:function(){return{sending:!1,comment:""}},methods:{prefill:function(e){e=e||"",this.comment=e,this.$els.textarea.setSelectionRange(e.length,e.length),this.$els.textarea.focus()},submit:function(){var e=this;this.sending=!0,this.$api.post("discussions/"+this.discussionId+"/",{comment:this.comment}).then(function(t){e.$dispatch("discussion:updated",t),e.comment="",e.sending=!1,document.location.href="#discussion-"+e.discussionId+"-"+(t.discussion.length-1)}).catch(function(t){var s=e._("An error occured while submitting your comment");e.$dispatch("notify.error",s),o.default.error(t),e.sending=!1})}}}},308:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(14),o=_interopRequireDefault(i),a=s(336),n=_interopRequireDefault(a),r=s(338),d=_interopRequireDefault(r),u=s(10),c=_interopRequireDefault(u),l=s(69);_interopRequireDefault(l);t.default={components:{ThreadMessage:n.default,ThreadForm:d.default},props:{discussion:Object,position:Number},data:function(){return{detailed:!0,formDisplayed:!1,currentUser:o.default.user}},events:{"discussion:updated":function(e){return this.hideForm(),!0}},computed:{discussionIdAttr:function(){return"discussion-"+this.discussion.id},createdDate:function(){return(0,c.default)(this.discussion.created).format("LL")},closedDate:function(){return(0,c.default)(this.discussion.closed).format("LL")}},methods:{toggleDiscussions:function(){this.detailed=!this.detailed},displayForm:function(){this.$auth(this._("You need to be logged in to comment.")),this.formDisplayed=!0,this.detailed=!0},hideForm:function(){this.formDisplayed=!1},start:function(e){var t=this;this.displayForm(),this.$nextTick(function(){t.$els.form&&t.$refs.form&&(t.$scrollTo(t.$els.form),t.$refs.form.prefill(e))})},focus:function(e){var t=this;this.detailed=!0,e?this.$nextTick(function(){t.$scrollTo("#"+t.discussionIdAttr+"-"+e)}):this.$scrollTo(this)}}}},309:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(122),o=_interopRequireDefault(i),a=s(14),n=_interopRequireDefault(a),r=s(69),d=_interopRequireDefault(r),u=s(339),c=_interopRequireDefault(u),l=s(337),p=_interopRequireDefault(l),f=s(5),m=_interopRequireDefault(f),b=/^#discussion-([0-9a-f]{24})$/,h=/^#discussion-([0-9a-f]{24})-(\d+)$/,v=/^#discussion-([0-9a-f]{24})-new-comment$/;t.default={components:{Avatar:d.default,DiscussionThread:c.default,ThreadFormCreate:p.default},data:function(){return{discussions:[],loading:!0,formDisplayed:!1,currentUser:n.default.user}},props:{subjectId:String,subjectClass:String},events:{"discussion:created":function(e){var t=this;this.hideForm(),this.discussions.unshift(e),this.$nextTick(function(){var s=t.threadFor(e.id);s.detailed=!0,t.$scrollTo(s)})},"discussion:updated":function(e){var t=this.discussions.indexOf(this.discussions.find(function(t){return t.id==e.id}));this.discussions.$set(t,e)}},ready:function(){var e=this;this.$api.get("discussions/",{for:this.subjectId}).then(function(t){e.loading=!1,e.discussions=t.data,document.location.hash&&e.$nextTick(function(){e.jumpToHash(document.location.hash)})}).catch(m.default.error.bind(m.default))},methods:{displayForm:function(){this.$auth(this._("You need to be logged in to start a discussion.")),this.formDisplayed=!0},hideForm:function(){this.formDisplayed=!1},start:function(e,t){var s=this;this.displayForm(),this.$nextTick(function(){s.$els.form&&s.$refs.form&&(s.$scrollTo(s.$els.form),s.$refs.form.prefill(e,t))})},threadFor:function(e){return this.$refs.threads.find(function(t){return t.discussion.id==e})},sortBy:function(e){"created"===e?this.discussions.sort(function(e,t){return new Date(t.created)-new Date(e.created)}):"response"===e&&this.discussions.sort(function(e,t){return new Date(t.discussion.slice(-1)[0].posted_on)-new Date(e.discussion.slice(-1)[0].posted_on)})},jumpToHash:function(e){if("#discussion-create"===e)this.start();else if(b.test(e)){var t=e.match(b),s=(0,o.default)(t,2),i=s[1];this.threadFor(i).focus()}else if(h.test(e)){var a=e.match(h),n=(0,o.default)(a,3),r=n[1],d=n[2];this.threadFor(r).focus(d)}else if(v.test(e)){var u=e.match(v),c=(0,o.default)(u,2),l=c[1];this.threadFor(l).start()}}}}},320:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,"","",{version:3,sources:[],names:[],mappings:"",file:"share.vue",sourceRoot:"webpack://"}])},321:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".discussion-message{display:flex;flex-direction:row;padding-top:1.25em}.discussion-message>.avatar{margin-right:1em;flex-basis:auto}.discussion-message .message-content{display:flex;flex-direction:column;min-width:0}.discussion-message .message-content .message-header{display:flex;flex:0 0 auto;margin-bottom:.5em}.discussion-message .message-content .message-header .author{flex:1 0 auto;font-weight:700}.discussion-message .message-content .message-header .posted_on{flex:0 0 auto;text-align:right}.discussion-message .message-content .message-header .posted_on .fa{margin-left:5px}.discussion-message .message-content .body{flex:1 0 auto}.discussion-message .message-content .body a,.discussion-message .message-content .body code{word-wrap:break-word;word-break:break-all}.discussion-message .message-content .body pre code{word-wrap:normal;word-break:normal}@media only screen and (max-width:480px){.avatar img{width:32px;height:32px}}","",{version:3,sources:["/./js/components/discussions/message.vue"],names:[],mappings:"AAAA,oBAAoB,aAAa,mBAAmB,kBAAkB,CAAC,4BAA4B,iBAAiB,eAAe,CAAC,qCAAqC,aAAa,sBAAsB,WAAW,CAAC,qDAAqD,aAAa,cAAc,kBAAkB,CAAC,6DAA6D,cAAc,eAAgB,CAAC,gEAAgE,cAAc,gBAAgB,CAAC,oEAAoE,eAAe,CAAC,2CAA2C,aAAa,CAAC,6FAA6F,qBAAqB,oBAAoB,CAAC,oDAAoD,iBAAiB,iBAAiB,CAAC,yCAAyC,YAAY,WAAW,WAAW,CAAC,CAAC",file:"message.vue",sourcesContent:[".discussion-message{display:flex;flex-direction:row;padding-top:1.25em}.discussion-message>.avatar{margin-right:1em;flex-basis:auto}.discussion-message .message-content{display:flex;flex-direction:column;min-width:0}.discussion-message .message-content .message-header{display:flex;flex:0 0 auto;margin-bottom:.5em}.discussion-message .message-content .message-header .author{flex:1 0 auto;font-weight:bold}.discussion-message .message-content .message-header .posted_on{flex:0 0 auto;text-align:right}.discussion-message .message-content .message-header .posted_on .fa{margin-left:5px}.discussion-message .message-content .body{flex:1 0 auto}.discussion-message .message-content .body a,.discussion-message .message-content .body code{word-wrap:break-word;word-break:break-all}.discussion-message .message-content .body pre code{word-wrap:normal;word-break:normal}@media only screen and (max-width:480px){.avatar img{width:32px;height:32px}}"],sourceRoot:"webpack://"}])},322:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".discussion-threads .list-group-form{height:inherit}.discussion-threads .list-group-form form{padding:1em}","",{version:3,sources:["/./js/components/discussions/threads.vue"],names:[],mappings:"AAAA,qCAAqC,cAAc,CAAC,0CAA0C,WAAW,CAAC",file:"threads.vue",sourcesContent:[".discussion-threads .list-group-form{height:inherit}.discussion-threads .list-group-form form{padding:1em}"],sourceRoot:"webpack://"}])},323:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".panel .panel-heading[_v-67a4da23]{padding:10px 15px;cursor:pointer}.read-more[_v-67a4da23]{text-align:center;cursor:pointer}.add-comment[_v-67a4da23]{padding:10px 15px}.add-comment>button.btn[_v-67a4da23]{margin:0 auto;display:block}","",{version:3,sources:["/./js/components/discussions/thread.vue"],names:[],mappings:"AAAA,mCAAmC,kBAAkB,cAAc,CAAC,wBAAwB,kBAAkB,cAAc,CAAC,0BAA0B,iBAAiB,CAAC,qCAAqC,cAAc,aAAa,CAAC",file:"thread.vue",sourcesContent:[".panel .panel-heading[_v-67a4da23]{padding:10px 15px;cursor:pointer}.read-more[_v-67a4da23]{text-align:center;cursor:pointer}.add-comment[_v-67a4da23]{padding:10px 15px}.add-comment>button.btn[_v-67a4da23]{margin:0 auto;display:block}"],sourceRoot:"webpack://"}])},324:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".sort[_v-debbe940]{margin-top:-32px;margin-bottom:1em;text-align:right}.loading[_v-debbe940]{margin:2em;text-align:center}.discussion-card.add[_v-debbe940]{cursor:pointer}.discussion-card.add .card-logo[_v-debbe940]{background-color:#eee;font-size:2em;display:flex;justify-content:center;align-items:center;height:60px}.discussion-card.add .card-body[_v-debbe940]{min-height:auto;justify-content:left}.discussion-card.add .card-body h4[_v-debbe940]{margin-bottom:0}.create>div[_v-debbe940]:first-child{display:flex;flex-direction:row}.create>div:first-child>div[_v-debbe940]:nth-child(3){padding:0 1em}.create>div:first-child .control[_v-debbe940]{text-align:right;width:4em;order:3}.create>div:first-child .control a[_v-debbe940]:hover{cursor:pointer}","",{version:3,sources:["/./js/components/discussions/threads.vue"],names:[],mappings:"AAAA,mBAAmB,iBAAiB,kBAAkB,gBAAgB,CAAC,sBAAsB,WAAW,iBAAiB,CAAC,kCAAkC,cAAc,CAAC,6CAA6C,sBAAyB,cAAc,aAAa,uBAAuB,mBAAmB,WAAW,CAAC,6CAA6C,gBAAgB,oBAAoB,CAAC,gDAAgD,eAAe,CAAC,qCAAqC,aAAa,kBAAkB,CAAC,sDAAsD,aAAa,CAAC,8CAA8C,iBAAiB,UAAU,OAAO,CAAC,sDAAsD,cAAc,CAAC",file:"threads.vue",sourcesContent:[".sort[_v-debbe940]{margin-top:-32px;margin-bottom:1em;text-align:right}.loading[_v-debbe940]{margin:2em;text-align:center}.discussion-card.add[_v-debbe940]{cursor:pointer}.discussion-card.add .card-logo[_v-debbe940]{background-color:#eeeeee;font-size:2em;display:flex;justify-content:center;align-items:center;height:60px}.discussion-card.add .card-body[_v-debbe940]{min-height:auto;justify-content:left}.discussion-card.add .card-body h4[_v-debbe940]{margin-bottom:0}.create>div[_v-debbe940]:first-child{display:flex;flex-direction:row}.create>div:first-child>div[_v-debbe940]:nth-child(3){padding:0 1em}.create>div:first-child .control[_v-debbe940]{text-align:right;width:4em;order:3}.create>div:first-child .control a[_v-debbe940]:hover{cursor:pointer}"],sourceRoot:"webpack://"}])},327:function(e,t){e.exports=' <a class=avatar :href=user.url :title="user | display"> <img class=avatar :src="user | avatar_url size" :alt="user | display" :width=size :height=size> </a> '},328:function(e,t){e.exports=' <button type=button class="btn btn-primary btn-share" :title="_(\'Share\')" v-tooltip v-popover popover-large :popover-title="_(\'Share\')"> <span class="fa fa-share-alt"></span> <div class="btn-group btn-group-lg" data-popover-content> <a class="btn btn-link" title=Google+ @click=click href="https://plus.google.com/share?url={{url|encode}}" target=_blank> <span class="fa fa-2x fa-google-plus"></span> </a> <a class="btn btn-link" title=Twitter @click=click href="https://twitter.com/home?status={{title|encode}}%20-%20{{url|encode}}" target=_blank> <span class="fa fa-2x fa-twitter"></span> </a> <a class="btn btn-link" title=Facebook @click=click href="https://www.facebook.com/sharer/sharer.php?u={{url|encode}}" target=_blank> <span class="fa fa-2x fa-facebook"></span> </a> <a class="btn btn-link" title=LinkedIn @click=click href="https://www.linkedin.com/shareArticle?mini=true&url={{url|encode}}&title={{title|encode}}" target=_blank> <span class="fa fa-2x fa-linkedin"></span> </a> </div> </button> '},329:function(e,t){e.exports=' <div class=discussion-message> <div class=avatar> <a href="{{ message.posted_by.page }}"><avatar :user=message.posted_by></avatar></a> </div> <div class=message-content> <div class=message-header> <div class=author> <a href="{{ message.posted_by.page }}">{{ message.posted_by | display }}</a> </div> <div class=posted_on> {{ formatDate(message.posted_on) }} <a href="#{{ discussion }}-{{ index }}"><span class="fa fa-link"></span></a> </div> </div> <div class=body> {{{ message.content | markdown }}} </div> </div> </div> '},330:function(e,t){e.exports=" <form role=form class=animated @submit.prevent=submit> <div class=form-group> <label for=title-new-discussion>{{ _('Title') }}</label> <input v-el:title type=text id=title-new-discussion v-model=title class=form-control required/> <label for=comment-new-discussion>{{ _('Comment') }}</label> <textarea v-el:textarea id=comment-new-discussion v-model=comment class=form-control rows=3 required></textarea> </div> <button type=submit :disabled=\"this.sending || !this.title || !this.comment\" class=\"btn btn-primary btn-block submit-new-discussion\"> {{ _('Start a discussion') }} </button> </form> "},331:function(e,t){e.exports=' <form role=form class="clearfix animated" @submit.prevent=submit> <div class=form-group> <label for=comment-new-message>{{ _(\'Comment\') }}</label> <textarea v-el:textarea id=comment-new-message v-model=comment class=form-control rows=3 required></textarea> </div> <button type=submit :disabled="this.sending || !this.comment" class="btn btn-primary btn-block pull-right submit-new-message"> {{ _(\'Submit your comment\') }} </button> </form> '},332:function(e,t){e.exports=' <div class="discussion-thread panel panel-default" _v-67a4da23=""> <div class=panel-heading @click=toggleDiscussions _v-67a4da23=""> <div _v-67a4da23=""> <a href="#{{ discussionIdAttr }}" class=pull-right v-on:click.stop="" _v-67a4da23=""><span class="fa fa-link" _v-67a4da23=""></span></a> <strong _v-67a4da23="">{{ discussion.title }}</strong> <span class="label label-warning" v-if=discussion.closed _v-67a4da23=""><i class="fa fa-minus-circle" aria-hidden=true _v-67a4da23=""></i> {{ _(\'closed discussion\') }}</span> </div> </div> <div class=list-group v-show=detailed _v-67a4da23=""> <thread-message v-for="(index, response) in discussion.discussion" id="{{ discussionIdAttr }}-{{ index }}" :discussion=discussionIdAttr :index=index :message=response class=list-group-item _v-67a4da23=""> </thread-message></div> <div class=add-comment v-show="detailed &amp;&amp; !discussion.closed" _v-67a4da23=""> <button v-show="!formDisplayed &amp;&amp; detailed &amp;&amp; !discussion.closed" type=button class="btn btn-primary" @click=displayForm _v-67a4da23=""> {{ _(\'Add a comment\') }} </button> <div v-el:form="" id="{{ discussionIdAttr }}-new-comment" v-show="formDisplayed &amp;&amp; currentUser" class="animated form" _v-67a4da23=""> <thread-form v-ref:form="" :discussion-id=discussion.id _v-67a4da23=""></thread-form> </div> </div> <div class="panel-footer read-more" v-show=!detailed @click=toggleDiscussions _v-67a4da23=""> <span class=text-muted _v-67a4da23="">{{ discussion.discussion.length }} {{ _(\'messages\') }}</span> </div> <div class=panel-footer v-if=discussion.closed _v-67a4da23=""> <div class=text-muted _v-67a4da23=""> {{ _(\'Discussion has been closed\') }} {{ _(\'by\') }} <a href="{{ discussion.closed_by.page }}" _v-67a4da23="">{{ discussion.closed_by | display }}</a> {{ _(\'on\') }} {{ closedDate }} </div> </div> </div> '},333:function(e,t){e.exports=' <div class=discussion-threads _v-debbe940=""> <div class=loading v-if=loading _v-debbe940=""> <i class="fa fa-spinner fa-pulse fa-2x fa-fw" _v-debbe940=""></i> <span class=sr-only _v-debbe940="">{{ _(\'Loading\') }}...</span> </div> <div class=sort v-show="discussions.length > 1" _v-debbe940=""> <div class=btn-group _v-debbe940=""> <button class="btn btn-default btn-sm dropdown-toogle" type=button data-toggle=dropdown aria-haspopup=true aria-expanded=false _v-debbe940=""> {{ _(\'sort by\') }} <span class=caret _v-debbe940=""></span> </button> <ul class="dropdown-menu dropdown-menu-right" _v-debbe940=""> <li _v-debbe940=""><a class=by_created @click="sortBy(\'created\')" _v-debbe940="">{{ _(\'topic creation\') }}</a></li> <li _v-debbe940=""><a class=last_response @click="sortBy(\'response\')" _v-debbe940="">{{ _(\'last response\') }}</a></li> </ul> </div> </div> <discussion-thread v-ref:threads="" v-for="discussion in discussions" :discussion=discussion id="discussion-{{ discussion.id }}" track-by=id _v-debbe940=""> </discussion-thread> <a class="card discussion-card add" @click=displayForm v-show=!formDisplayed _v-debbe940=""> <div class=card-logo _v-debbe940=""><span _v-debbe940="">+</span></div> <div class=card-body _v-debbe940=""> <h4 _v-debbe940="">{{ _(\'Start a new discussion\') }}</h4> </div> </a> <div v-el:form="" id=discussion-create v-show=formDisplayed v-if=currentUser class="create list-group-item animated" _v-debbe940=""> <div _v-debbe940=""> <div class=avatar _v-debbe940=""> <avatar :user=currentUser _v-debbe940=""></avatar> </div> <div class=control _v-debbe940=""> <a href=#discussion-create _v-debbe940=""><span class="fa fa-link" _v-debbe940=""></span></a> <a @click=hideForm _v-debbe940=""><span class="fa fa-times" _v-debbe940=""></span></a> </div> <div _v-debbe940=""> <h4 class=list-group-item-heading _v-debbe940=""> {{ _(\'Starting a new discussion thread\') }} </h4> <p class=list-group-item-text _v-debbe940=""> {{ _("You\'re about to start a new discussion thread. Make sure that a thread about the same topic doesn\'t exist yet just above.") }} </p> </div> </div> <thread-form-create v-ref:form="" :subject-id=subjectId :subject-class=subjectClass _v-debbe940=""></thread-form-create> </div> </div> '},335:function(e,t,s){var i,o;s(342),i=s(304),o=s(328),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},336:function(e,t,s){var i,o;s(343),i=s(305),o=s(329),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},337:function(e,t,s){var i,o;i=s(306),o=s(330),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},338:function(e,t,s){var i,o;i=s(307),o=s(331),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},339:function(e,t,s){var i,o;s(345),i=s(308),o=s(332),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},340:function(e,t,s){var i,o;s(346),s(344),i=s(309),o=s(333),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},342:function(e,t,s){var i=s(320);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},343:function(e,t,s){var i=s(321);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},344:function(e,t,s){var i=s(322);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},345:function(e,t,s){var i=s(323);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},346:function(e,t,s){var i=s(324);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},424:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(5),o=_interopRequireDefault(i);t.default={props:{subjectId:String,subjectType:String,featured:Boolean,compact:Boolean},methods:{toggleFeatured:function(){var e=this;this.$role("admin");var t=this.featured?"delete":"post",s=this.subjectType.toLowerCase()+"s/"+this.subjectId+"/featured/";this.$api[t](s).then(function(t){e.featured=!e.featured}).catch(o.default.error.bind(o.default))}}}},425:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(75),o=_interopRequireDefault(i);t.default={props:{title:{type:String,required:!0},objectType:{type:String,required:!0},objectId:{type:String,required:!0},widgetUrl:{type:String,required:!0},rootUrl:String,documentationUrl:String},data:function(){return{help:this._("Copy-paste this code within your own HTML at the place you want the current dataset to appear:"),tooltip:this._("Click the button to copy the whole code within your clipboard"),documentation:this._("Read the documentation to insert more than one dataset")}},computed:{snippet:function(){var e="script",t=this.rootUrl&&!this.widgetUrl.startsWith(this.rootUrl)?' data-udata="'+this.rootUrl+'"':"";return"<div data-udata-"+this.objectType+'="'+this.objectId+'"></div>\n<'+e+t+' src="'+this.widgetUrl+'" async defer></'+e+">"}},methods:{click:function(){this.$els.textarea.select(),document.execCommand("copy"),o.default.publish("INTEGRATE")}}}},426:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(508),o=_interopRequireDefault(i);t.default={props:{subjectId:{type:String,required:!0},subjectClass:{type:String,required:!0},count:{type:Number,default:0,coerce:parseInt}},methods:{click:function(){this.$root.$modal(o.default,{subject:{id:this.subjectId,class:this.subjectClass}})}}}},429:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(5),o=_interopRequireDefault(i),a=s(69),n=_interopRequireDefault(a);t.default={components:{Avatar:n.default},props:{issue:{type:Object,required:!0}},data:function(){return{comment:""}},computed:{canSubmit:function(){return this.comment&&!this.sending}},methods:{submitComment:function(){this.submit(!1,this._("Your comment has been sent to the team"),this._("An error occured while submitting your comment"))},submitCommentAndClose:function(){this.submit(!0,this._("The issue has been closed"),this._("An error occured while closing the issue"))},submit:function(e,t,s){var i=this;this.$auth(this._("You need to be logged in to submit a comment.")),this.canSubmit&&this.$api.post("issues/"+this.issue.id+"/",{close:e,comment:this.comment}).then(function(e){i.comment="",i.sending=!1,i.$dispatch("issue:updated",e),i.$dispatch("notify:success",t)}).catch(function(e){i.$dispatch("notify:error",s),o.default.error(e),i.sending=!1})}}}},430:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(69),o=_interopRequireDefault(i);t.default={components:{Avatar:o.default},props:{subject:{type:Object,required:!0}},data:function(){return{loading:!0,issues:[]}},ready:function(){var e=this;this.$api.get("issues/",{for:this.subject.id}).then(function(t){e.issues=t.data,e.loading=!1})}}},431:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(5),o=_interopRequireDefault(i);t.default={props:{subject:{type:Object,required:!0}},data:function(){return{sending:!1,title:"",comment:""}},computed:{canSubmit:function(){return this.title&&this.comment&&!this.sending}},methods:{submit:function(){var e=this;this.canSubmit&&(this.sending=!0,this.$api.post("issues/",{title:this.title,comment:this.comment,subject:this.subject}).then(function(t){e.title="",e.comment="",e.sending=!1,e.$dispatch("issue:created",t),e.$dispatch("notify:success",e._("Your issue has been sent to the team"))}).catch(function(t){e.$dispatch("notify:error",e._("An error occured while submitting your issue")),o.default.error(t),e.sending=!1}))}}}},432:function(e,t,s){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(t,"__esModule",{value:!0});var i=s(10),o=_interopRequireDefault(i),a=s(121),n=_interopRequireDefault(a),r=s(75),d=(_interopRequireDefault(r),s(505)),u=_interopRequireDefault(d),c=s(507),l=_interopRequireDefault(c),p=s(506),f=_interopRequireDefault(p);t.default={components:{Modal:n.default,List:f.default,New:l.default,Display:u.default},props:{subject:{type:Object,required:!0}},data:function(){return{view:"list",issue:null}},computed:{title:function(){return"display"===this.view?this.issue.title+" <small>("+this.issueDate+")</small>":"new"===this.view?this._("New issue"):this._("Issues")},issueDate:function(){if(this.issue)return(0,o.default)(this.issue.created).format("LLL")}},events:{new:function(){this.$auth(this._("You need to be logged in to submit a new issue.")),this.view="new"},close:function(){this.$refs.modal.close()},back:function(){this.issue=null,this.view="list"},"issue:selected":function(e){this.issue=e,this.view="display"},"issue:created":function(e){this.issue=e,this.view="display"},"issue:updated":function(e){this.issue=e}}}},477:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".integrate-popover .integrate-popover-wrapper{width:100%;display:flex;align-items:center}.integrate-popover textarea{width:100%}","",{version:3,sources:["/./js/components/buttons/integrate.vue"],names:[],mappings:"AAAA,8CAA8C,WAAW,aAAa,kBAAkB,CAAC,4BAA4B,UAAU,CAAC",file:"integrate.vue",sourcesContent:[".integrate-popover .integrate-popover-wrapper{width:100%;display:flex;align-items:center}.integrate-popover textarea{width:100%}"],sourceRoot:"webpack://"}])},480:function(e,t,s){t=e.exports=s(6)(),t.push([e.id,".media{margin-top:15px}.media:first-child{margin-top:0}.media,.media-body{overflow:hidden;zoom:1}.media-body{width:10000px}.media-object{display:block}.media-object.img-thumbnail{max-width:none}.media-right,.media>.pull-right{padding-left:10px}.media-left,.media>.pull-left{padding-right:10px}.media-body,.media-left,.media-right{display:table-cell;vertical-align:top}.media-middle{vertical-align:middle}.media-bottom{vertical-align:bottom}.media-heading{margin-top:0;margin-bottom:5px}.media-list{padding-left:0;list-style:none}.issues-list .issue{margin-top:15px;overflow:hidden;zoom:1;background-color:#eee;cursor:pointer}.issues-list .issue .media-body{padding:5px}.issues-list .issue:first-child{margin-top:0}","",{version:3,sources:["/./js/components/issues/object-modal-list.vue"],names:[],mappings:"AAAA,OAAO,eAAe,CAAC,mBAAmB,YAAY,CAAC,mBAAmB,gBAAgB,MAAM,CAAC,YAAY,aAAa,CAAC,cAAc,aAAa,CAAC,4BAA4B,cAAc,CAAC,gCAAgC,iBAAiB,CAAC,8BAA8B,kBAAkB,CAAC,qCAAqC,mBAAmB,kBAAkB,CAAC,cAAc,qBAAqB,CAAC,cAAc,qBAAqB,CAAC,eAAe,aAAa,iBAAiB,CAAC,YAAY,eAAe,eAAe,CAAC,oBAAoB,gBAAgB,gBAAgB,OAAO,sBAAsB,cAAc,CAAC,AAA6C,gCAAgC,WAAW,CAAC,gCAAgC,YAAY,CAAC",file:"object-modal-list.vue",sourcesContent:[".media{margin-top:15px}.media:first-child{margin-top:0}.media,.media-body{overflow:hidden;zoom:1}.media-body{width:10000px}.media-object{display:block}.media-object.img-thumbnail{max-width:none}.media-right,.media>.pull-right{padding-left:10px}.media-left,.media>.pull-left{padding-right:10px}.media-left,.media-right,.media-body{display:table-cell;vertical-align:top}.media-middle{vertical-align:middle}.media-bottom{vertical-align:bottom}.media-heading{margin-top:0;margin-bottom:5px}.media-list{padding-left:0;list-style:none}.issues-list .issue{margin-top:15px;overflow:hidden;zoom:1;background-color:#eee;cursor:pointer}.issues-list .issue:first-child{margin-top:0}.issues-list .issue .media-body{padding:5px}.issues-list .issue:first-child{margin-top:0}"],
sourceRoot:"webpack://"}])},488:function(e,t){e.exports=" <button type=button class=\"btn featured\" :class=\"{active: featured, 'btn-success': !compact, 'btn-default': compact}\" @click=toggleFeatured v-tooltip=\"_('Feature this content')\" tooltip-placement=top> <span class=\"fa fa-bullhorn\"></span> <span v-if=!compact>{{ _('Featured') }}</span> </button> "},489:function(e,t){e.exports=' <button type=button class="btn btn-primary btn-integrate" :title=title v-tooltip v-popover popover-large :popover-title="_(\'Share\')"> <span class="fa fa-code"></span> <div data-popover-content> <div class=integrate-popover> <p>{{ help }}</p> <div class=integrate-popover-wrapper> <textarea readonly=readonly rows=4 v-el:textarea>{{ snippet }}</textarea> <a class="btn btn-link" @click=click :title=tooltip v-tooltip tooltip-placement=bottom> <span class="fa fa-3x fa-clipboard"></span> </a> </div> <p v-if=documentationUrl> <span class="fa fa-question-circle"><a :href=documentationUrl>{{documentation}}</a></span> </p> </div> </div> </button> '},490:function(e,t){e.exports=' <button type=button class="btn btn-danger btn-issues" @click=click v-tooltip tooltip-placement=top :title="_(\'Issues\')"> <span class="fa fa-warning"></span> <span v-if=count class=count>{{ count }}</span> </button> '},493:function(e,t){e.exports=' <div class=issue-details> <div class=modal-body> <div class=media v-for="comment in issue.discussion"> <a class=pull-left :href=comment.posted_by.page> <avatar :user=comment.posted_by></avatar> </a> <div class=media-body> <div class="message text-left"> <p>{{{ comment.content|markdown }}}</p> </div> </div> </div> <form role=form :action=issue.url> <div class=form-group> <label for=comment>{{ _(\'Comment\') }}</label> <textarea id=comment v-model=comment class=form-control rows=3 required></textarea> </div> </form> </div> <footer class="modal-footer text-center"> <button class="btn btn-primary" @click=submitComment :disabled=!canSubmit> <span class="fa fa-comment"></span> {{ _(\'Comment\') }} </button> <button class="btn btn-primary" @click=submitCommentAndClose :disabled=!canSubmit> <span class="fa fa-comments-o"></span> {{ _(\'Comment and close\') }} </button> <button class="btn btn-info" @click="$dispatch(\'back\')" :disabled=sending> <span class="fa fa-step-backward"></span> {{ _(\'Back\') }}  <button type=button class="btn btn-default" @click="$dispatch(\'close\')" :disabled=sending> <span class="fa fa-times"></span> {{ _(\'Close\') }} </button> </button></footer> </div> '},494:function(e,t){e.exports=' <div class=issues-list> <div class=modal-body> <div class="tab-pane fade in active" v-if="loading && !issues.length"> <div class="text-center spinner-container"> <i class="fa fa-2x fa-refresh fa-spin"></i> </div> </div> <div class=issue v-for="issue in issues" @click="$dispatch(\'issue:selected\', issue)"> <div class=pull-left> <avatar :user=issue.user></avatar> </div> <div class=media-body> <h4 class="media-heading text-left">{{issue.title}}</h4> <i>{{ issue.created|dt }}</i> </div> </div> <p v-if="!loading && !issues.length" class=text-center>{{ _(\'No issue.\') }}</p> <p v-if="!loading && !issues.length" class=text-center>{{ _(\'Click on new issue if you want to emit a new one.\') }}</p> </div> <footer class="modal-footer text-center"> <button class="btn btn-primary" @click="$dispatch(\'new\')"> <span class="fa fa-plus"></span> {{ _(\'New issue\') }} </button> <button type=button class="btn btn-default" @click="$dispatch(\'close\')"> <span class="fa fa-times"></span> {{ _(\'Close\') }} </button> </footer> </div> '},495:function(e,t){e.exports=' <div class=new-issue-form> <div class=modal-body> <p><strong>{{ _("You\'re about to submit a new issue related to a tendencious usage of the platform, illegal data opened or shameless advertisement. Note that questions and discussions about the data itself now takes place in the community section of each dataset.") }}</strong></p> <form role=form> <div class=form-group> <label for=title>{{ _(\'Title\') }}</label> <input type=text id=title v-model=title class=form-control required :disabled=sending /> </div> <div class=form-group> <label for=comment>{{ _(\'Details\') }}</label> <textarea id=comment v-model=comment class=form-control rows=3 required :disabled=sending></textarea> </div> </form> </div> <footer class="modal-footer text-center"> <button class="btn btn-primary" @click=submit :disabled=!canSubmit> <span class="fa fa-check"></span> {{ _(\'Submit\') }} </button> <button class="btn btn-info" @click="$dispatch(\'back\')" :disabled=sending> <span class="fa fa-step-backward"></span> {{ _(\'Back\') }} </button> <button type=button class="btn btn-default" @click="$dispatch(\'close\')" :disabled=sending> <span class="fa fa-times"></span> {{ _(\'Close\') }} </button> </footer> </div> '},496:function(e,t){e.exports=" <modal class=object-issues-modal v-ref:modal :title=title> <component :is=view v-ref:view :subject=subject :issue=issue></component> </modal> "},500:function(e,t,s){var i,o;i=s(424),o=s(488),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},501:function(e,t,s){var i,o;s(512),i=s(425),o=s(489),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},502:function(e,t,s){var i,o;i=s(426),o=s(490),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},505:function(e,t,s){var i,o;i=s(429),o=s(493),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},506:function(e,t,s){var i,o;s(515),i=s(430),o=s(494),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},507:function(e,t,s){var i,o;i=s(431),o=s(495),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},508:function(e,t,s){var i,o;i=s(432),o=s(496),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),o&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=o)},512:function(e,t,s){var i=s(477);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},515:function(e,t,s){var i=s(480);"string"==typeof i&&(i=[[e.id,i,""]]);s(7)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},977:984});
//# sourceMappingURL=reuse.a12cde4c0631dbee48fd.js.map