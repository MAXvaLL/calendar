import React, { useEffect } from 'react';
import { HashRouter } from 'react-router-dom';
import Pullable from 'react-pullable';
import ScrollRestoration from 'components/ScrollRestoration/ScrollRestoration';
import 'styles/reset.css';
import ZoomControl from 'components/ZoomControl/ZoomControl';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Plugins } from '@capacitor/core';
import { useSetRecoilState } from 'recoil';
import pendingUpdateState from 'state/pendingUpdateState';
import checkVersion from 'checkVersion';
import precache from 'precache';
import isDarkMode from 'utils/isDarkMode';

import Routes from '../Routes';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnMount: false,
            refetchOnWindowFocus: false,
            refetchOnReconnect: false,
        },
    },
});

export default () => {
    const setPendingUpdate = useSetRecoilState(pendingUpdateState);
    useEffect(() => {
        const loader = document.getElementById('loader');
        const reactRoot = document.getElementById('react-root');
        if (loader && reactRoot) {
            loader.style.display = 'none';
            reactRoot.style.display = 'block';
        }
        Plugins.SplashScreen.hide();
    }, []);
    const dark = isDarkMode();
    return (
        <QueryClientProvider client={queryClient}>
            <HashRouter>
                <ScrollRestoration />
                <Pullable
                    spinnerColor={dark ? '#fff' : '#000'}
                    onRefresh={async () => {
                        const newVersion = await checkVersion();
                        if (newVersion) {
                            setPendingUpdate(newVersion);
                        }
                        await precache(true);
                        await queryClient.refetchQueries();
                    }}
                >
                    <Routes />
                </Pullable>
            </HashRouter>
            <ZoomControl />
        </QueryClientProvider>
    );
};
