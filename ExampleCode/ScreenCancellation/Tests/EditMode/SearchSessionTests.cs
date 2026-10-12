using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using NUnit.Framework;
using UnityEngine;

namespace UnityBestPractices.Samples.Cancellation.Tests
{
    public sealed class SearchSessionTests
    {
        [Test]
        public async Task SupersededRequest_CannotReplaceTheNewerResult()
        {
            ControlledSearchService service = new ControlledSearchService();
            using (SearchSession session = new SearchSession(service))
            {
                int notifications = 0;
                session.ResultChanged += result => notifications++;
                Awaitable oldRequest = session.SearchAsync("old");
                Awaitable newRequest = session.SearchAsync("new");
                Assert.That(service.Tokens[0].IsCancellationRequested, Is.True);
                service.Results[1].SetResult("new result");
                await newRequest;
                service.Results[0].SetResult("late old result");
                await oldRequest;
                Assert.That(session.Result, Is.EqualTo("new result"));
                Assert.That(notifications, Is.EqualTo(1));
            }
        }

        [Test]
        public async Task ClosedSession_CannotAffectAReopenedSession()
        {
            ControlledSearchService service = new ControlledSearchService();
            SearchSession oldSession = new SearchSession(service);
            Awaitable oldRequest = oldSession.SearchAsync("old");
            oldSession.Dispose();
            oldSession.Dispose();
            Assert.That(service.Tokens[0].IsCancellationRequested, Is.True);
            using (SearchSession newSession = new SearchSession(service))
            {
                Awaitable newRequest = newSession.SearchAsync("new");
                service.Results[0].SetResult("late");
                await oldRequest;
                Assert.That(oldSession.Result, Is.Empty);
                Assert.That(newSession.Result, Is.Empty);
                service.Results[1].SetResult("current");
                await newRequest;
                Assert.That(newSession.Result, Is.EqualTo("current"));
            }
        }

        [Test]
        public async Task ProviderFailure_PropagatesToTheOperationOwner()
        {
            ControlledSearchService service = new ControlledSearchService();
            using (SearchSession session = new SearchSession(service))
            {
                Awaitable request = session.SearchAsync("failure");
                service.Results[0].SetException(new InvalidOperationException("Provider failed"));
                try
                {
                    await request;
                    Assert.Fail("Provider failures must be observed by the caller.");
                }
                catch (InvalidOperationException exception)
                {
                    Assert.That(exception.Message, Is.EqualTo("Provider failed"));
                }
                Assert.That(session.Result, Is.Empty);
            }
        }

        private sealed class ControlledSearchService : ISearchService
        {
            public List<AwaitableCompletionSource<string>> Results { get; } =
                new List<AwaitableCompletionSource<string>>();
            public List<CancellationToken> Tokens { get; } = new List<CancellationToken>();

            public Awaitable<string> SearchAsync(string query, CancellationToken cancellationToken)
            {
                AwaitableCompletionSource<string> source = new AwaitableCompletionSource<string>();
                Results.Add(source);
                Tokens.Add(cancellationToken);
                // Deliberately ignore cancellation to exercise the stale-result guard.
                return source.Awaitable;
            }
        }
    }
}
